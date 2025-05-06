const shortenText = (text, maxLength = 20, appendix = "...") => {
    return text.length > maxLength? text.slice(0, maxLength)+appendix: text;
};

const getCoursesForSelection = async () => {
    try {
        const response = await fetch("/api/admin/courses", {
            method: "GET"
        });
        const data = await response.json();
        console.log(data.courses);
        return data.courses;
    } catch (err) {
        console.error("Error getting courses:", err);
        return []; 
    }
};

export {shortenText, getCoursesForSelection};