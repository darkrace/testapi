window.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll('[role="tab"]');
    const tabList = document.querySelector('[role="tablist"]');

    // Add a click event handler to each tab
    tabs.forEach(tab => {
        tab.addEventListener("click", changeTabs);
    });

});

function changeTabs(e) {
    const target = e.target;
    const parent = target.parentNode;
    const grandparent = parent.parentNode;

    // Remove all current selected tabs
    parent
        .querySelectorAll('[aria-selected="true"]')
        .forEach(t => t.setAttribute("aria-selected", false));

    parent
        .querySelectorAll('[aria-selected="false"]')
        .forEach(t => t.classList.remove("tab-c"));



    // Set this tab as selected
    target.setAttribute("aria-selected", true);
    if (target.getAttribute("aria-selected")) {
        target.classList.add("tab-c");
    }
    // Hide all tab panels
    grandparent
        .querySelectorAll('[role="tabpanel"]')
        .forEach(p => p.setAttribute("hidden", true));

    // Show the selected panel
    grandparent.parentNode
        .querySelector(`#${target.getAttribute("aria-controls")}`)
        .removeAttribute("hidden");
}