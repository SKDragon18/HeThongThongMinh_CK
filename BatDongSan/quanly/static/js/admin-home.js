// Lấy các phần tử HTML cần xử lý
const collapseButton = document.getElementById("collapse-button");
const sidebarMenu = document.querySelector(".sidebar-menu");
const themeSwitch = document.getElementById("theme-switch");
const pageContent = document.querySelector(".page-content");
const searchButton = document.getElementById("search-button");
const searchInput = document.getElementById("search-input");
const editButtons = document.querySelectorAll(".edit-button");
const deleteButtons = document.querySelectorAll(".delete-button");
const approveButtons = document.querySelectorAll(".approve-button");

// Viết hàm xử lý sự kiện thu gọn sidebar
function collapseSidebar() {
    // Nếu sidebar đang mở rộng, thu gọn nó và ẩn các mục quản lý
    if (sidebarMenu.style.display !== "none") {
        sidebarMenu.style.display = "none";
        // Thay đổi nội dung của nút thu gọn thành "Mở rộng"
        collapseButton.innerHTML = "Mở rộng";
    } else {
        // Nếu sidebar đang thu gọn, mở rộng nó và hiển thị các mục quản lý
        sidebarMenu.style.display = "block";
        // Thay đổi nội dung của nút thu gọn thành "Thu gọn"
        collapseButton.innerHTML = "Thu gọn";
    }
}