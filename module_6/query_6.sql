SELECT fullname
FROM students
WHERE group_id = (SELECT id FROM groups WHERE groups.id = 1);