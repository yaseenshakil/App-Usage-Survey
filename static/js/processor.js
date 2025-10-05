function toggleInput(event){
    let checkBox = document.getElementById("feedbackCheckbox")
    let textArea = document.getElementById("moreInfo")
    let textAreaLabel = document.getElementById("moreInfoLabel")
    console.log(checkBox.checked)
    if (checkBox.checked){
        console.log("Setting attribute to block")
        textArea.style.display = "block"
        textAreaLabel.style.display = "block"
    }
    else{
        textArea.style.display = "none"
        textAreaLabel.style.display = "none"

    }

}

