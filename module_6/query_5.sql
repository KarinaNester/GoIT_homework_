SELECT subjects.name AS course_name
FROM subjects
WHERE subjects.teacher_id = (SELECT id FROM teachers WHERE id = 2);