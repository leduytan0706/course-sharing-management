const imagePreview = document.getElementsByClassName("course-image-preview")[0];
const imageInput = document.getElementById("courseImage");
const addCourseForm = document.getElementsByClassName("add-course-form")[0];
const addLessonBtn = document.getElementsByClassName("add-lesson-btn")[0];
const rmLessonBtn = document.getElementsByClassName("course-lesson-delete")[0];
const lessons = document.getElementsByClassName("course-lesson-list")[0];
let numberOfLessons = 1;

document.addEventListener("DOMContentLoaded", async () => {
    const newLesson = `<div class="course-lesson-card">
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
    const newLessonNode = document.createElement('div');
    newLessonNode.innerHTML = newLesson;
    lessons.appendChild(newLessonNode);
});

imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      imagePreview.src = url;
    }
});

addLessonBtn.addEventListener('click',  () => {
    numberOfLessons++;
    const newLesson = `<div class="course-lesson-card">
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
    const newLessonNode = document.createElement('div');
    newLessonNode.innerHTML = newLesson;
    lessons.appendChild(newLessonNode);
});

rmLessonBtn.addEventListener('click', () => {

});

addCourseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Course added successfully!');

    const numberOfLessons = parseInt(addCourseForm.elements['numOfLessons'].value);

    const formData = new FormData();

    // Thêm thông tin khóa học
    formData.append('name', addCourseForm.elements['courseName'].value);
    formData.append('intro', addCourseForm.elements['courseIntro'].value);
    formData.append('image', addCourseForm.elements['courseImage'].files[0]); // Lưu ý .files[0]
    formData.append('number_of_lessons', numberOfLessons);
    formData.append('category', addCourseForm.elements['courseCategory'].value);
    formData.append('level', addCourseForm.elements['courseLevel'].value);
    formData.append('description', addCourseForm.elements['courseDescription'].value);

    // Thêm từng bài học
    for (let i = 1; i <= numberOfLessons; i++) {
        const name = addCourseForm.elements[`lessonName_${i}`].value;
        const video = addCourseForm.elements[`lessonVideo_${i}`].files[0];
        const content = addCourseForm.elements[`lessonContent_${i}`].value;

        formData.append(`lessons[${i}][name]`, name);
        formData.append(`lessons[${i}][video]`, video);
        formData.append(`lessons[${i}][content]`, content);
    }

    // Gửi lên backend
    fetch('/api/admin/courses/new', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload success:', data);
        const newCourseId = data.course_id;
        window.location.href = '/admin/courses/'+newCourseId;
    })
    .catch(err => console.error('Error:', err));

    
});


const validateAddCourseForm = () => {

}