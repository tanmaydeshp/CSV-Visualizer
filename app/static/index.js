function delete_file(fileID) {
    fetch("/delete_file/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
    },
      body: JSON.stringify({ fileID: fileID })
    }).then((_res) => {
      window.location.href = "/myfiles/";
    });
  }

function download_file(filename){
  fetch("/download_file/", {method:"POST", headers:{"Content-Type": "application/json",}, body: JSON.stringify({filename:filename})}).then((_res) => window.location.href = "/myfiles/")
}