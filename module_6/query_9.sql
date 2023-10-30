SELECT subjects.name AS course_name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE grades.student_id = (SELECT id FROM students WHERE students.id = 1);