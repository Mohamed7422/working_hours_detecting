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
            title: title ,
            text:  message ,
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

 function showSuccessAlert(title){
  Swal.fire({
    title: title,
    icon: "success",
    draggable: true
  });
 }
// Attach the function to the global window object
window.showAlert = showAlert;
window.showSuccessAlert = showSuccessAlert;


