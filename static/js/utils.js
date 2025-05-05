const shortenText = (text, maxLength = 20, appendix = "...") => {
    return text.length > maxLength? text.slice(0, maxLength)+appendix: text;
};

export {shortenText};