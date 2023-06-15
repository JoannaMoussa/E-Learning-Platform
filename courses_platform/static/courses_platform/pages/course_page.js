$(document).ready( function () {
    $('#myTable').DataTable({
        columns: [
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
                    if (type === "sort") {
                        if (data === "Passed") {
                            return 1;
                        } else if (data === "Enrolled") {
                            return 0;
                        }
                    }
                    return data; // this return is for the filter case
                }
            },
        ]
    });
} );