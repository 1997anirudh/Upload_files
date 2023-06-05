// Function to handle the file drop event
function handleFileDrop(event) {
    event.preventDefault();
    var files = event.dataTransfer.files;
    handleFiles(files);
}

// Function to handle the file selection event
function handleFileSelect(event) {
    var files = event.target.files;
    handleFiles(files);
}

// Function to handle the uploaded files
function handleFiles(files) {
    var fileInput = document.getElementById('fileInput');
    fileInput.files = files;
    document.getElementById('fileLabel').textContent = fileInput.files[0].name;
}

// Register drag and drop events
var dropArea = document.getElementById('dropArea');
dropArea.addEventListener('dragover', function(event) {
    event.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', function(event) {
    event.preventDefault();
    dropArea.classList.remove('dragover');
    var files = event.dataTransfer.files;
    handleFiles(files);
});

// Register file input change event
var fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', function(event) {
    handleFileSelect(event);
});
