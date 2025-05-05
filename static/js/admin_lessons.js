import { shortenText } from "./utils.js";

const lessonsTableBody = document.getElementById("lessons-table-body");
const backdropContainer = document.getElementById("backdrop");
const backdropModal = document.getElementById("modal");
let lessonTableRows;
const confirmBtn = document.querySelectorAll("confirm-btn");

document.addEventListener("DOMContentLoaded", async () => {
    let lessonsRow = ``;

    await fetch("/api/admin/lessons", {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data.lessons
    })
    .then(lessonsData => {
        lessonsData.forEach((lesson,index) => {
            const lessonRow = `<tr class="lessons-table-data" data-index="${index}" id="lessonId-${lesson.id}">
                    <td class="align-left">${index+1}</td>
                    <td class="align-left">${shortenText(lesson.name, 40)}</td>
                    <td class="align-left">${lesson.content}</td>
                    <td class="align-center">${new Date(lesson.created_at).toLocaleDateString()}</td>
                    <td class="align-center">
                        <a href="/admin/lessons/update/${lesson.id}" class="lesson-edit-btn">
                            <i class='bx bx-pencil edit-icon'></i>
                        </a>
                        <button type="button" class="lesson-delete-btn">
                            <i class="bx bx-trash delete-icon"></i>
                        </button>
                    </td>
                </tr>`;

            lessonsRow += lessonRow;
        });

        
        lessonsTableBody.innerHTML = lessonsRow;

        lessonTableRows = lessonsTableBody.childNodes;

        handleLessonClick();

        handleLessonDeleteBtns();

        handleLessonCancelBtns();
    })
    .catch((err) => {
        console.log(err);
    }); 
    
});

const handleLessonDeleteBtns = () => {
    const courseDeleteBtns = document.querySelectorAll(".lesson-delete-btn");
    courseDeleteBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            backdropContainer.classList.toggle("backdrop-show");
            backdropModal.innerHTML=`<div class="lesson-delete-card">
                <div class="card-header"></div>
                <div class="card-content">
                    <div class="card-content-title">
                        <h4 class="card-content-text">Are you sure you want to delete this lesson?</h4>
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

const handleLessonCancelBtns = () => {
    const cancelBtn = document.querySelectorAll("cancel-btn");
    cancelBtn.forEach(btn => {
        btn.addEventListener('click', () => {
            backdropModal.classList.toggle("modal-hidden");
            backdropContainer.classList.toggle("backdrop-show");
        });
    });
};

const handleLessonClick = () => {
    lessonTableRows.forEach(lessonRow => {
        lessonRow.addEventListener("click", () => {
            const lessonId = lessonRow.id.split("-")[1];
            console.log(lessonId);
            window.location.href = '/admin/lessons/'+lessonId;
        })
    })
}

