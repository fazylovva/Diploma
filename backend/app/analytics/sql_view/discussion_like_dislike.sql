CREATE OR REPLACE VIEW discussion_likes_dislikes AS
SELECT 
  d.id, 
  d.comment, 
  COALESCE(likes.likes_count, 0) AS likes,
  COALESCE(dislikes.dislikes_count, 0) AS dislikes
FROM "Discussion" d
LEFT JOIN (
  SELECT 
    discussion_id,
    COUNT(*) AS likes_count
  FROM "Discussion_like"
  GROUP BY discussion_id
) likes ON d.id = likes.discussion_id
LEFT JOIN (
  SELECT 
    discussion_id,
    COUNT(*) AS dislikes_count
  FROM "Discussion_dislike"
  GROUP BY discussion_id
) dislikes ON d.id = dislikes.discussion_id;
