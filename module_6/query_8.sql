SELECT subjects.name AS subject_name, AVG(grades.grade) AS average_grade
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE subjects.teacher_id = (SELECT id FROM teachers WHERE teachers.id = 1)
GROUP BY subjects.name;
