// The fetchData function can be found on the "movieresults.html" page. It is an "onclick" function. 
async function fetchData(event){

    try{

        const movie_id = event.target.getAttribute('data-movie_id');
        
// This looks for the data-movie_id attribute's value. It knows to look for the correct value, because 
// it associates the "event" with whichever plus sign was clicked. NOTE: The plus sign is referred to as 
// "bi bi-plus" in the code.

        const response = await fetch(`[Your ords/mymovies/movie-single/ endpoint goes here]${movie_id}`);

// When you add your ORDS URI above, you'll need to remove the ":id" portion. You DO want to keep the 
// ${movie_id} expression though. That will allow you to pass the movie_id as a route parameter. If you review the handler code 
// in the REST Workshop, you'll see how this is being passed to the database.

        console.log(response);
        if(!response.ok){
            throw new Error("Could not fetch resource");
        }
        const data = await response.json();

// The NumberFormat code below formats the Gross Sales value so it appears as a USD currency. It also makes the assumption that 
// null is 0. Technically, this is incorrect. Some of the values in the MOVIES table are null. I assume they were never recorded. 
// So you may want to pay attention to that if you decide to "extend" this application.

        const formatter = Intl.NumberFormat('en-US', {
            style:  'currency',
            currency: 'USD'
        });
        
        grossSales = formatter.format(Number(data.gross));

// The below line takes the JSON response, "const data = ...." and passes it back to the "movieresults.html" page to display in the 
// Modal's title field.
        
        document.querySelector(".modal-title").innerHTML = data.title;

// Here you'll see more templating. These are called "Template Literals." And they allow you to pass the HTML and any expressions - ${expression} - back 
// to the html template. In this case, we are passing back the Summary and Gross Sales information. See the notes.md page for a 
// Template Literal reference.
        
        document.querySelector(".modal-body").innerHTML = 
       `<div class="container">
            <h6>Summary</h6>
            <div class="row">
                <p class="fw-light">${data.summary}</p>
            </div>
            <h6>Gross Sales</h6>
            <div class="row">
                <p class="fw-light">${grossSales}</p>
            </div>
        </div>`
    }
    catch(error){
        console.error(error);
        
    };
};
