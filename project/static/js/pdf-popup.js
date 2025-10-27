document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.pdf-popup-link').forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault(); // stop normal navigation
            const url = link.href;
            const popup = window.open(
                url,
                '_blank', // open in a new window/tab
                // 'PDFPopup', if you want to use the same window (give it a name and remove the blank line above)
                'width=1000,height=800,toolbar=no,menubar=no,scrollbars=yes,resizable=yes'
            );

            if (!popup || popup.closed || typeof popup.closed === 'undefined') {
                // fallback if popup blocked
                window.location.href = url;
            }
        });
    });
});