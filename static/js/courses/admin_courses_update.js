const imagePreview = document.getElementsByClassName("course-image-preview")[0];
const imageInput = document.getElementById("courseImage");
const updateCourseForm = document.getElementsByClassName("update-course-form")[0];
const updateLessonBtn = document.getElementsByClassName("update-lesson-btn")[0];
const rmLessonBtns = document.getElementsByClassName("course-lesson-delete");
const lessonContainer = document.getElementsByClassName("course-lesson-list")[0];
let courseId = null;
let numberOfLessons = 1;

document.addEventListener("DOMContentLoaded", async () => {
    const pathParts = window.location.pathname.split('/');
    courseId = pathParts[pathParts.length - 1];

    console.log("Course ID:", courseId); // "1"
    let courseData;
    fetch('/api/admin/courses/'+courseId, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Course data:', data);
        const courseData = data.course;
        numberOfLessons = courseData.lessons.length;
        const courseLessons = courseData.lessons;
        let existingLessons = ``;

        // assign course data
        updateCourseForm.elements["courseName"].value=courseData.name || "";
        updateCourseForm.elements["courseIntro"].value=courseData.intro || "";
        updateCourseForm.elements["numOfLessons"].value=courseData.number_of_lessons || "";
        updateCourseForm.elements["courseCategory"].value=courseData.category.name || "";
        updateCourseForm.elements["courseLevel"].value=courseData.level || "";
        updateCourseForm.elements["courseDescription"].value=courseData.description || "";
        console.log(courseData.image_url);
        imagePreview.src=courseData.image_url || "";

        // asign existing lessons data
        for (let i=0;i<numberOfLessons;i++){
            existingLessons = existingLessons + `
            <div class="course-lesson-card" id="lesson${i+1}">
                <div class="lesson-card-header">
                    <span class="course-lesson-number">Lesson ${i+1}</span>
                    <i class='bx bx-x course-lesson-delete lesson-${i+1}'></i>
                </div>
                <div class="form-field lesson-name-field">
                    <label for="lessonName_${i+1}" class="form-label">
                        <span class="field-name lesson-name">Lesson Name</span>
                        <input 
                            type="text"
                            id="lessonName_${i+1}"
                            name="lessonName_${i+1}"
                            class="form-input lesson-name-input"
                            placeholder="Enter the name of this lesson"
                            value="${courseLessons[i].name || ""}"
                        />
                    </label>
                    
                </div>
                <div class="form-field lesson-video-field">
                    <label for="lessonVideo_${i+1}" class="form-label">
                        <span class="field-name lesson-video">Lesson Video</span>
                        <input 
                            type="file"
                            id="lessonVideo_${i+1}"
                            name="lessonVideo_${i+1}"
                            class="form-input lesson-video-input"
                            accept="video/*"
                        />
                        <video 
                            id="videoPreview" 
                            class="lesson-video-preview" 
                            style="display: none;"
                            controls 
                            width="400"
                            value="${courseLessons[i].video_url || ""}">
                        </video>
                    </label>
                    
                </div>
                <div class="form-field lesson-content-field">
                    <label for="lessonContent_${i+1}" class="form-label">
                        <span class="field-name lesson-name">Lesson Content</span>
                        <textarea 
                            id="lessonContent_${i+1}"
                            name="lessonContent_${i+1}"
                            class="form-input lesson-content-input"
                            cols="100" 
                            rows="7" 
                            value=""
                        >
                            ${courseLessons[i].content || ""}
                        </textarea>

                    </label>
                    
                </div>
            </div>`
        }

            lessonContainer.insertAdjacentHTML('beforeend', existingLessons);
        })
    .catch(err => console.error('Error:', err));

    
});

imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      imagePreview.src = url;
    }
});

updateLessonBtn.addEventListener('click',  () => {
    numberOfLessons++;
    const newLesson = `<div class="course-lesson-card" id="lesson${numberOfLessons}" data-index="${numberOfLessons}">
                    <div class="lesson-card-header">
                        <span class="course-lesson-number">Lesson ${numberOfLessons}</span>
                        <i class='bx bx-x course-lesson-delete lesson-${numberOfLessons}'></i>
                    </div>
                    <div class="form-field lesson-name-field">
                        <label for="lessonName_${numberOfLessons}" class="form-label">
                            <span class="field-name lesson-name">Lesson Name</span>
                            <input 
                                type="text"
                                id="lessonName_${numberOfLessons}"
                                name="lessonName_${numberOfLessons}"
                                class="form-input lesson-name-input"
                                placeholder="Enter the name of this lesson"
                            />
                        </label>
                        
                    </div>
                    <div class="form-field lesson-video-field">
                        <label for="lessonVideo_${numberOfLessons}" class="form-label">
                            <span class="field-name lesson-video">Lesson Video</span>
                            <input 
                                type="file"
                                id="lessonVideo_${numberOfLessons}"
                                name="lessonVideo_${numberOfLessons}"
                                class="form-input lesson-video-input"
                                accept="video/*"
                            />
                            <video 
                                id="videoPreview" 
                                class="lesson-video-preview" 
                                style="display: none;"
                                controls 
                                width="400">
                            </video>
                        </label>
                        
                    </div>
                    <div class="form-field lesson-content-field">
                        <label for="lessonContent_${numberOfLessons}" class="form-label">
                            <span class="field-name lesson-name">Lesson Content</span>
                            <textarea 
                                id="lessonContent_${numberOfLessons}"
                                name="lessonContent_${numberOfLessons}"
                                class="form-input lesson-content-input"
                                cols="100" 
                                rows="7" 
                            >
                            </textarea>

                        </label>
                        
                    </div>`
    lessonContainer.insertAdjacentHTML('beforeend', newLesson);
});

const updateLessonOrder = () => {
    const lessonDivs = document.querySelectorAll(".course-lesson-card");
    lessonDivs.forEach((lesson, index) => {
        const newIndex = index + 1;
        lesson.setAttribute('data-index', newIndex);
        lesson.querySelector('.course-lesson-number').textContent = `Lesson ${newIndex}`;
        lesson.querySelector('.lesson-name-input').id = `lessonName_${newIndex}`;
        lesson.querySelector('.lesson-name-input').name = `lessonName_${newIndex}`;
        lesson.querySelectorAll('.form-label')[0].htmlFor = `lessonName_${newIndex}`;

        lesson.querySelector('.lesson-video-input').id = `lessonVideo_${newIndex}`;
        lesson.querySelector('.lesson-name-input').name = `lessonVideo_${newIndex}`;
        lesson.querySelectorAll('.form-label')[1].htmlFor = `lessonVideo_${newIndex}`;

        lesson.querySelector('.lesson-content-input').id = `lessonContent_${newIndex}`;
        lesson.querySelector('.lesson-content-input').name = `lessonContent_${newIndex}`;
        lesson.querySelectorAll('.form-label')[2].htmlFor = `lessonContent_${newIndex}`;
    });
};

const handleDeleteLesson = (e) => {
    numberOfLessons--;
    const lessonDiv = e.target.closest(".course-lesson-card");
    lessonDiv.remove();
    updateLessonOrder();
};

lessonContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('course-lesson-delete')) {
        handleDeleteLesson(e);
    }
});

updateCourseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    

    const numOfLessons = parseInt(updateCourseForm.elements['numOfLessons'].value) || numberOfLessons;
    console.log(numOfLessons);

    const formData = new FormData();

    // Thêm thông tin khóa học
    formData.append('name', updateCourseForm.elements['courseName'].value);
    formData.append('intro', updateCourseForm.elements['courseIntro'].value);
    formData.append('image', updateCourseForm.elements['courseImage'].files[0]); // Lưu ý .files[0]
    formData.append('number_of_lessons', numberOfLessons);
    formData.append('category', updateCourseForm.elements['courseCategory'].value);
    formData.append('level', updateCourseForm.elements['courseLevel'].value);
    formData.append('description', updateCourseForm.elements['courseDescription'].value);

    // Thêm từng bài học
    for (let i = 1; i <= numberOfLessons; i++) {
        const name = updateCourseForm.elements[`lessonName_${i}`].value;
        const video = updateCourseForm.elements[`lessonVideo_${i}`].files[0];
        const content = updateCourseForm.elements[`lessonContent_${i}`].value;

        formData.append(`lessons[${i}][name]`, name);
        formData.append(`lessons[${i}][video]`, video);
        formData.append(`lessons[${i}][content]`, content);
    }

    // Gửi lên backend
    fetch('/api/admin/courses/update/'+courseId, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload success:', data);
        const updatedCourseId = data.course_id;
        window.location.href = '/admin/courses/'+updatedCourseId;
    })
    .catch(err => console.error('Error:', err));

    alert('Course added successfully!');
});


const validateAddCourseForm = () => {

}