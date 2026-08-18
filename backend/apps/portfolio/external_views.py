"""
External coding-profile fetchers — GitHub and LeetCode.

Fetched server-side (not directly from the browser) because:
- LeetCode's GraphQL endpoint rejects requests without browser-like headers
  and has no public CORS allowance for arbitrary origins.
- Caching here keeps every page view from hitting GitHub/LeetCode directly,
  which matters given GitHub's 60 req/hour unauthenticated rate limit.

/api/github-profile/   — GET, cached GitHub profile + top starred repos
/api/leetcode-profile/ — GET, cached LeetCode profile + solve stats
"""
import json
import urllib.error
import urllib.request

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

GITHUB_USERNAME = 'sushant1058git'
LEETCODE_USERNAME = 'sushant1058jan'
CACHE_TTL = 60 * 60  # 1 hour

GITHUB_CACHE_KEY = 'external_github_profile'
LEETCODE_CACHE_KEY = 'external_leetcode_profile'

LEETCODE_QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      reputation
      starRating
      userAvatar
      realName
      aboutMe
      countryName
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}
"""


def _fetch_json(url, method='GET', data=None, headers=None, timeout=8):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _fetch_github_profile():
    headers = {'User-Agent': 'sushant-portfolio-app', 'Accept': 'application/vnd.github+json'}
    profile = _fetch_json(f'https://api.github.com/users/{GITHUB_USERNAME}', headers=headers)
    repos = _fetch_json(
        f'https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=stars&direction=desc&per_page=6',
        headers=headers,
    )
    top_repos = [
        {
            'name': r.get('name'),
            'description': r.get('description'),
            'url': r.get('html_url'),
            'stars': r.get('stargazers_count', 0),
            'forks': r.get('forks_count', 0),
            'language': r.get('language'),
            'updated_at': r.get('updated_at'),
        }
        for r in repos
    ]
    return {
        'username': profile.get('login'),
        'name': profile.get('name'),
        'avatar_url': profile.get('avatar_url'),
        'bio': profile.get('bio'),
        'company': profile.get('company'),
        'location': profile.get('location'),
        'blog': profile.get('blog'),
        'html_url': profile.get('html_url'),
        'public_repos': profile.get('public_repos', 0),
        'followers': profile.get('followers', 0),
        'following': profile.get('following', 0),
        'created_at': profile.get('created_at'),
        'top_repos': top_repos,
    }


def _fetch_leetcode_profile():
    payload = json.dumps({
        'query': LEETCODE_QUERY,
        'variables': {'username': LEETCODE_USERNAME},
    }).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Referer': f'https://leetcode.com/{LEETCODE_USERNAME}/',
        'Origin': 'https://leetcode.com',
        'User-Agent': 'Mozilla/5.0 (compatible; sushant-portfolio-app)',
    }
    data = _fetch_json('https://leetcode.com/graphql', method='POST', data=payload, headers=headers)
    matched = data.get('data', {}).get('matchedUser')
    if not matched:
        raise ValueError('LeetCode user not found')
    stats = {row['difficulty']: row['count'] for row in matched['submitStats']['acSubmissionNum']}
    profile = matched.get('profile') or {}
    return {
        'username': matched.get('username'),
        'ranking': profile.get('ranking'),
        'avatar_url': profile.get('userAvatar'),
        'about_me': profile.get('aboutMe'),
        'country': profile.get('countryName'),
        'solved': {
            'all': stats.get('All', 0),
            'easy': stats.get('Easy', 0),
            'medium': stats.get('Medium', 0),
            'hard': stats.get('Hard', 0),
        },
        'profile_url': f'https://leetcode.com/u/{LEETCODE_USERNAME}/',
    }


class GitHubProfileView(APIView):
    def get(self, request):
        data = cache.get(GITHUB_CACHE_KEY)
        if data is not None:
            return Response(data)
        try:
            data = _fetch_github_profile()
        except (urllib.error.URLError, ValueError, KeyError) as e:
            return Response({'error': f'Could not fetch GitHub profile: {e}'}, status=502)
        cache.set(GITHUB_CACHE_KEY, data, CACHE_TTL)
        return Response(data)


class LeetCodeProfileView(APIView):
    def get(self, request):
        data = cache.get(LEETCODE_CACHE_KEY)
        if data is not None:
            return Response(data)
        try:
            data = _fetch_leetcode_profile()
        except (urllib.error.URLError, ValueError, KeyError) as e:
            return Response({'error': f'Could not fetch LeetCode profile: {e}'}, status=502)
        cache.set(LEETCODE_CACHE_KEY, data, CACHE_TTL)
        return Response(data)
