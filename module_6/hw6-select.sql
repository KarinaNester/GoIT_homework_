#1
SELECT
    s.id, 
    s.fullname, 
    ROUND(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 5;


#2
WITH StudentGrades AS (
    SELECT 
        s.id,
        s.fullname,
        ROUND(AVG(g.grade)) as average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    WHERE g.subject_id = 1  -- Предмет, з якого ви хочете знайти середній бал
    GROUP BY s.id
)
SELECT 
    id, 
	fullname, 
    average_grade
FROM StudentGrades
ORDER BY average_grade DESC
LIMIT 1;

SELECT 
    s.id, 
    s.fullname, 
    ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
where g.subject_id = 1
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 1;

#3

SELECT students.group_id, AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.id = 2
GROUP BY students.group_id;


#4
SELECT AVG(grade) AS average_grade
FROM grades;


#5
SELECT subjects.name AS course_name
FROM subjects
WHERE subjects.teacher_id = (SELECT id FROM teachers WHERE fullname = 'Bradley Alexander');

#6
SELECT fullname
FROM students
WHERE group_id = (SELECT id FROM groups WHERE name = 'within');


#7
SELECT students.fullname AS student_name, grades.grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.group_id = (SELECT id FROM groups WHERE name = 'born')
  AND subjects.name = 'office';


#8
SELECT subjects.name AS subject_name, AVG(grades.grade) AS average_grade
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE subjects.teacher_id = (SELECT id FROM teachers WHERE fullname = 'Bradley Alexander')
GROUP BY subjects.name;


#9
SELECT subjects.name AS course_name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE grades.student_id = (SELECT id FROM students WHERE fullname = 'Nathan Murphy');

#10
SELECT subjects.name AS course_name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
JOIN students ON grades.student_id = students.id
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE students.fullname = 'Nathan Murphy'
  AND teachers.fullname = 'Bradley Alexander';
