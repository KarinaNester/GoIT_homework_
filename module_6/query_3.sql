SELECT students.group_id, AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.id = 2
GROUP BY students.group_id;