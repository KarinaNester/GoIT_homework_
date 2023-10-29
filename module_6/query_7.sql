SELECT students.fullname AS student_name, grades.grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.group_id = (SELECT id FROM groups WHERE name = 'born')
  AND subjects.name = 'office';