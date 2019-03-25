#standardSQL
SELECT
  committer.name,
  committer.email,
  COUNT(*) AS commit_count
FROM
  `bigquery-public-data.github_repos.commits`
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 100