document.addEventListener("DOMContentLoaded", () => {
  const dateButton = document.getElementById("date");
  const dateFilter = document.getElementById("date_filter");
  const accountButton = document.getElementById("account");
  const accountFilter = document.getElementById("account_filter");
  const categoryButton = document.getElementById("category");
  const categoryFilter = document.getElementById("category_filter");

  // Check if elements exist before adding event listeners
  if (!accountButton || !accountFilter ) {
    console.error("Account filter elements not found in DOM");
    return;
  }
  
  if (!categoryButton || !categoryFilter) {
    console.error("Category filter elements not found in DOM");
    return;
  }

    if (!dateButton || !dateFilter) {
    console.error("Date filter elements not found in DOM");
    return;
  }

  // Display Date filter
  function openDate() {
    dateFilter.hidden = false;
  }

  function closeDate() {
    dateFilter.hidden = true;
  }

  // Display Category filter
  function openCategory() {
    categoryFilter.hidden = false;
  }

  function closeCategory() {
    categoryFilter.hidden = true;
  }

  // Display Account filter
  function openAccount() {
    accountFilter.hidden = false;
  }

  function closeAccount() {
    accountFilter.hidden = true;
  }

  // Date button click handler
  dateButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (dateFilter.hidden) {
      openDate();
    } else {
      closeDate();
    }
  });

  // Category button click handler
  categoryButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (categoryFilter.hidden) {
      openCategory();
    } else {
      closeCategory();
    }
  });

  // Account button click handler
  accountButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (accountFilter.hidden) {
      openAccount();
    } else {
      closeAccount();
    }
  });

  // Close filters when clicking outside
  document.addEventListener("click", (e) => {
    // Close date filter if clicking outside
    if (
      dateFilter && !dateFilter.hidden &&
      !dateFilter.contains(e.target) &&
      e.target !== dateButton
    ) {
      closeDate();
    }
    
    // Close category filter if clicking outside
    if (
      categoryFilter && !categoryFilter.hidden &&
      !categoryFilter.contains(e.target) &&
      e.target !== categoryButton
    ) {
      closeCategory();
    }
    
    // Close account filter if clicking outside
    if (
      accountFilter && !accountFilter.hidden &&
      !accountFilter.contains(e.target) &&
      e.target !== accountButton
    ) {
      closeAccount();
    }
  });

  // Close filters on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (dateFilter && !dateFilter.hidden) closeDate();
      if (categoryFilter && !categoryFilter.hidden) closeCategory();
      if (accountFilter && !accountFilter.hidden) closeAccount();
    }
  });
});
