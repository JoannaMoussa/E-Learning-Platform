$(document).ready( function () {
    $('#myTable').DataTable({
        columns: [
            {
                data: "Username",
                render: function (data, type) {
                    if (type === "display") {
                        let userId = data.split(",")[0];
                        let username = data.split(",")[1];
                        let link = `/profile/${userId}`

                        return '<a href="' + link + '">' + username + '</a>';
                    }
                    return username; // This will be used when sorting and filtering
                }
            },
            {
                data: "First Name",
            },
            {
                data: "Last Name",
            },
            {
                data: "Status",
                render: function (data, type) {
                    if (type === "display") {
                        if (data === "Passed") {
                            color = "green";
                        } else if (data === "Enrolled") {
                            color = "grey";
                        }
                        return '<span style="color:' + color + '">' + data + '</span>';
                    }
                    // This will be used when sorting
                    if (type === "sort") {
                        if (data === "Passed") {
                            return 1;
                        } else if (data === "Enrolled") {
                            return 0;
                        }
                    }
                    return data; // This will be used when filtering
                }
            },
        ]
    });
} );