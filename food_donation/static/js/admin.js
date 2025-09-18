document.addEventListener('DOMContentLoaded', function() {
            // Toggle dropdown menus
            document.querySelectorAll('.dropdown-toggle').forEach(function(toggle) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Close all other dropdowns
                    document.querySelectorAll('.dropdown-menu').forEach(function(menu) {
                        if (menu !== this.nextElementSibling) {
                            menu.classList.remove('show');
                        }
                    }.bind(this));
                    
                    // Toggle current dropdown
                    const dropdown = this.nextElementSibling;
                    dropdown.classList.toggle('show');
                    
                    // Rotate arrow
                    const arrow = this.querySelector('.down-arrow');
                    arrow.classList.toggle('fa-angle-down');
                    arrow.classList.toggle('fa-angle-up');
                });
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!event.target.matches('.dropdown-toggle') && !event.target.closest('.dropdown-menu')) {
                    document.querySelectorAll('.dropdown-menu').forEach(function(dropdown) {
                        dropdown.classList.remove('show');
                    });
                    
                    // Reset all arrows
                    document.querySelectorAll('.down-arrow').forEach(function(arrow) {
                        arrow.classList.add('fa-angle-down');
                        arrow.classList.remove('fa-angle-up');
                    });
                }
            });
            
            // Prevent dropdown from closing when clicking inside
            document.querySelectorAll('.dropdown-menu').forEach(function(menu) {
                menu.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });