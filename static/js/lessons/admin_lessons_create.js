const courseSelect = document.getElementById("courseName");
const addLessonForm = document.getElementsByClassName("add-lesson-form")[0];


document.addEventListener("DOMContentLoaded", async () => {
    let courses;
    try {
        courses = await getCoursesForSelection();
        if (!courses || courses.length <= 0){
            throw new Error("No courses found.")
        }
    } catch (error) {
        alert(`There was an error getting courses: {error.message}`);
        return;
    }
    
    let courseOptions = ``;
    for (let course of courses){
        courseOptions += `<option value="${course.id}">${course.name}</option>`
    }

    courseSelect.insertAdjacentHTML("beforeend", courseOptions);

});

const getCoursesForSelection = async () => {
    await fetch("/api/admin/courses", {
        "method": "GET"
    })
    .then (response => response.json())
    .then(data => {
        return data.courses;
    })
    .catch(err => {
        return err;
    })
};

addLessonForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData();

    formData.append('courseName',addLessonForm.elements['courseName'].value);
    formData.append('lessonName',addLessonForm.elements['lessonName'].value);
    formData.append('lessonContent',addLessonForm.elements['lessonContent'].value);
    formData.append('lessonVideo',addLessonForm.elements['lessonVideo'].files[0]);

    fetch('/api/admin/lessons/new', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload success: ', data);
        const newLessonId = data.lesson_id;
        alert('Lesson added successfully!');
        window.location.href = '/admin/lessons/'+newLessonId;
    })
    .catch(err => console.error(err));
    
});