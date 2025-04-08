const coursesTableBody = document.getElementById("courses-table-body");
const backdropContainer = document.getElementById("backdrop");
const backdropModal = document.getElementById("modal");

const confirmBtn = document.querySelectorAll("confirm-btn");

document.addEventListener("DOMContentLoaded", async () => {
    let coursesRow = ``;

    await fetch("/api/admin/courses", {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data.courses
    })
    .then(coursesData => {
        coursesData.forEach((course,index) => {
            const courseRow = `<tr class="courses-table-data" data-index="{{${index}}}">
                    <td class="align-left">1</td>
                    <td class="align-left">
                        <img 
                            src=${course.image_url || "/static/images/course_placeholder.svg"} 
                            alt="Course ${index}"
                        />
                    </td>
                    <td class="align-left">${course.name}</td>
                    <td class="align-center">${new Date(course.created_at).toLocaleDateString()}</td>
                    <td class="align-center">${course.status}</td>
                    <td class="align-center">
                        <a href="/admin/courses/update/${course.id}" class="course-edit-btn">
                            <i class='bx bx-pencil edit-icon'></i>
                        </a>
                        <button type="button" class="course-delete-btn">
                            <i class="bx bx-trash delete-icon"></i>
                        </button>
                    </td>
                </tr>`;

            coursesRow += courseRow;
        });
    })
    .catch((err) => {
        console.log(err);
    });

    coursesTableBody.innerHTML = coursesRow;

    handleCourseDeleteBtns();

    handleCourseCancelBtns();
    
});

const handleCourseDeleteBtns = () => {
    const courseDeleteBtns = document.querySelectorAll(".course-delete-btn");
    courseDeleteBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            backdropContainer.classList.toggle("backdrop-show");
            backdropModal.innerHTML=`<div class="course-delete-card">
                <div class="card-header"></div>
                <div class="card-content">
                    <div class="card-content-title">
                        <h4 class="card-content-text">Are you sure you want to delete this course?</h4>
                    </div>
                    <div class="card-content-action">
                        <button type="button" class="action-btn cancel-btn">Cancel</button>
                        <button type="button" class="action-btn confirm-btn">Delete</button>
                    </div>
                </div>
            </div>`;
            backdropModal.classList.toggle("modal-hidden");
        })
    });
};

const handleCourseCancelBtns = () => {
    const cancelBtn = document.querySelectorAll("cancel-btn");
    cancelBtn.forEach(btn => {
        btn.addEventListener('click', () => {
            backdropModal.classList.toggle("modal-hidden");
            backdropContainer.classList.toggle("backdrop-show");
        });
    });
};

