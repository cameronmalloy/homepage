document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector('.search-bar input');

    if (searchInput) {
        // Set the placeholder text
        searchInput.setAttribute('placeholder', 'Press [Q] to search...');
        
        // Add event listener for keydown on the document
        document.addEventListener('keydown', function(event) {
            // Check if the key pressed is 'q' or 'Q'
            if ((event.key === 'q' || event.key === 'Q') && 
                !event.ctrlKey && 
                !event.altKey && 
                !event.metaKey) {
                
                // Check if user is not already in an input field or textarea
                const activeElement = document.activeElement;
                const isInputActive = activeElement.tagName === 'INPUT' || 
                                     activeElement.tagName === 'TEXTAREA' || 
                                     activeElement.isContentEditable;
                
                if (!isInputActive) {
                    // Prevent default action of the key press
                    event.preventDefault();
                    
                    // Focus on the search input
                    searchInput.focus();
                    
                    // Optionally clear the input if it has any value
                    // searchInput.value = '';
                }
            }
        });
    } else {
        console.error('Search input not found on the page');
    }
  
    // // Set the placeholder when the page loads
    // searchInput.setAttribute("placeholder", "Press [Q] to search...");
  
    // // Focus on the input field when the page loads
    // searchInput.focus();

    // console.log(searchInput);
  
    // // When the user hits 'Enter', remove the placeholder text
    // searchInput.addEventListener('keydown', function (event) {
    //     console.log("Key Pressed:", event.key);
    //     // If the key pressed is 'q'
    //     if (event.key.toLowerCase() === "q") {
    //         console.log("Q key pressed, focusing search input");
    //         // Focus the search input
    //         inputElement.focus();
    //         // Clear the placeholder text
    //         inputElement.placeholder = "";
    //         // Set the value to "q"
    //         inputElement.value = "q";
    //         // Move the cursor to the end of the "q"
    //         inputElement.setSelectionRange(1, 1);
    // //   if (event.key === "q") {
    // //     searchInput.setAttribute("placeholder", ""); // Remove placeholder on enter
    // //     searchInput.focus(); // Focus the input field
    //   }
    // });
  });
  