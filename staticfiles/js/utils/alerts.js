function showAlert(type, title, message, options = {}) {
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: "btn btn-success",
      cancelButton: "btn btn-danger"
    },
    buttonsStyling: false
  });
  swalWithBootstrapButtons.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes",
    cancelButtonText: "No, cancel!",
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      swalWithBootstrapButtons.fire({
        title: title,
        text: message,
        icon: "success"
      });
    } else if (
      /* Read more about handling dismissals below */
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire({
        title: "Cancelled",
        text: "Your entries is not submitted yet)",
        icon: "error"
      });
    }
  });
}

function showSuccessAlert(title) {
  Swal.fire({
    title: title,
    icon: "success",
    draggable: true
  });
}

function showErrorAlert(message) {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: message,
  });
}

function showExceedingHoursAlert(message) {
  Swal.fire({
    icon: "warning",
    title: message,
    showClass: {
      popup: `
        animate__animated
        animate__fadeInUp
        animate__faster
      `
    },
    hideClass: {
      popup: `
        animate__animated
        animate__fadeOutDown
        animate__faster
      `
    },
    timer: 3000
  });
}

function showWarningNotification(message) {
  // Set the delay to 10 seconds
  alertify.set('notifier', 'delay', 10);

  // Set the position to top-right
  alertify.set('notifier', 'position', 'top-right');

  // Display the warning notification with a custom icon and bold text
  alertify.warning(`
    <div style="display: flex; align-items: center;">
      <i class="fas fa-exclamation-triangle" style="color: #ff9900; margin-right: 8px;"></i>
      <div>
        <strong style="color: #4d4d4d;">Warning!</strong> 
        <p style="margin: 0; font-size: 14px; color: #4d4d4d;">${message}</p>
      </div>
    </div>
  `);
}



// Attach the function to the global window object
window.showAlert = showAlert;
window.showSuccessAlert = showSuccessAlert;
window.showErrorAlert = showErrorAlert;
//window.showExceedingHoursAlert = showExceedingHoursAlert;
window.showWarningNotification = showWarningNotification;


