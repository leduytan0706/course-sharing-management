const categoriesContainer = document.getElementsByClassName("categories")[0];

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/category");
        const response = await res.json();
        const categories = response.categories;
        const categoriesRender = categories.map(category => `<li>${category.name}</li>`).join("");
        categoriesContainer.innerHTML = categoriesRender;

        let storeHTML = `<div class="address-box">
                    <div class="address-img">
                        <img src="" alt="" />
                    </div>
                    <h5></h5>
                    <a href="" target="_blank" class="map">Xem bản đồ</a>
                    <h5>Chia sẻ trên: <a href="#"><i class="bx bxl-facebook"></i></a> <a href="#"><i class='bx bx-link'></i></a></h5>
                    <p></p>
                    <p>07:00 - 22:00</p>
                    <p><i class='bx bx-car' ></i> Có chỗ để xe ô tô</p>
                    <p><i class='bx bx-shopping-bag'></i> Mua mang đi</p>
                    <p><i class='bx bx-store' ></i> Phục vụ tại chỗ</p>
                </div>`;
        document.getElementById("address").innerHTML = storeHTML;
    } catch (error) {
        console.log(error.message);
    }
});


