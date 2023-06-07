let titlesContainers;

document.addEventListener('DOMContentLoaded', () => {
    load_courses("title");

    const sortFilterBtn = document.getElementById("sort-filter-btn");
    const sortFilterBtnTxtComplement = document.getElementById("sort-filter-btn-txt-complement");
    const sortFilterCont = document.getElementById("sort-filter-cont");
    const sortFilterApplyBtn = document.getElementById("sort-filter-apply-btn");
    const sortFilterCloseBtn = document.getElementById("sort-filter-close-btn");
    const filterCont = document.getElementById("filter-options-cont");

    const cardsContainer = document.getElementById("cards-grid");
    const pageCover = document.getElementById("all-courses-cover");
    const searchInput = document.getElementById("search-query");

    searchInput.addEventListener("input", (e) => {
        let searchQuery = e.target.value;
        filterCoursesByQuery (searchQuery);
    })

    sortFilterBtn.addEventListener("click", () => {
        sortFilterCont.style.display = "flex";
        document.body.style.overflowY = "hidden";
        pageCover.style.display = "block";
    })

    sortFilterCloseBtn.addEventListener("click", () => {
        sortFilterCont.style.display = "none";
        document.body.style.overflowY = "auto";
        pageCover.style.display = "none";
    })

    sortFilterApplyBtn.addEventListener("click", (event) => {
        event.preventDefault(); //prevent form from being submitted
        // Get sort parameter
        let selectedRadioBtn = document.querySelector('input[name="sort-parameter"]:checked');
        if (selectedRadioBtn !== null) {
            sortBy = selectedRadioBtn.value
        } else {
            sortBy = "title"
        }
        // Get filter parameters
        let filterContChildren = filterCont.children;
        let filterData = {};
        for (let i = 1; i < filterContChildren.length; i += 2) {
            if (filterContChildren[i].value !== "") {
                filterData[filterContChildren[i].name] = filterContChildren[i].value
            }
        }
        cardsContainer.replaceChildren(); //Remove all existing cards
        load_courses(sortBy, filterData);
        sortFilterCont.style.display = "none";
        document.body.style.overflowY = "auto";
        pageCover.style.display = "none";
        // Add number of filters applied
        if (Object.keys(filterData).length === 0) {
            sortFilterBtnTxtComplement.innerHTML =  "";
        }
        else {
            sortFilterBtnTxtComplement.innerHTML = ` (${Object.keys(filterData).length})`;
        }
    })
});


function filterCoursesByQuery (search_query) {
    search_query = search_query.toLowerCase();
    titlesContainers.forEach(container => {
        if (!container.innerHTML.toLowerCase().includes(search_query)) {
            container.parentElement.style.display = "none";
        }
        else {
            container.parentElement.style.display = "flex";
        }
    })
}


function load_courses(sortParameter, filterDict={}) {
    // Add sorting data
    let uri = `/allCoursesApi?sort=${sortParameter}`;
    // Add filtering data
    if (Object.keys(filterDict).length !== 0) {
        let str = Object.keys(filterDict).map(function(key) {
            return key + "=" + filterDict[key];
          }).join('&');
        
        uri += `&${str}`;
    }

    let encoded_uri = encodeURI(uri);

    fetch(encoded_uri) 
    .then(response => {
        return response.json().then(json => {
            return response.ok ? json : Promise.reject(json.error);
        })
    })
    .then(allCourses => {
        allCourses.forEach((course) => {
            let temp = document.getElementById("cards-template");
            let course_card = temp.content.cloneNode(true);

            course_card.getElementById("card-anchor").setAttribute("href", `courses/${course.id}`);
            course_card.getElementById("card-img").setAttribute("src", course.image);
            course_card.getElementById("card-title").innerHTML = course.title;
            course_card.getElementById("card-duration").innerHTML = `${course.duration} weeks`;
            course_card.getElementById("card-level").innerHTML = `Level: ${course.level}`;

            document.getElementById("cards-grid").appendChild(course_card);
        })

        titlesContainers = document.querySelectorAll("#card-title");
        
        // filter courses by taking into acount the search query
        let searchQuery = document.getElementById("search-query").value;
        filterCoursesByQuery (searchQuery); 
    })
    .catch(error_msg => {
        console.log(error_msg)
    })
}
