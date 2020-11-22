document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(
                ".active"
            ).parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", (e) => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", (e) => {
                if (
                    e.target.classList.contains("btn") &&
                    e.target.parentElement.parentElement.classList.contains(
                        "help--slides-pagination"
                    )
                ) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach((btn) =>
                btn.firstElementChild.classList.remove("active")
            );
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach((el) => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * Callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            let page = e.target.dataset.page;
            let csrftoken = Cookies.get("csrftoken");
            let kind = document.querySelector("div.help--slides.active").dataset
                .id;

            function truncate(str) {
                return str.length > 110 ? str.substr(0, 110) + "&hellip;" : str;
            }

            $.ajax({
                type: "POST",
                url: "/",
                data: {
                    kind: kind - 1,
                    page: page,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function (data) {
                    let current_slide_ul = document.querySelector(
                        "div.help--slides.active ul.help--slides-items"
                    );
                    current_slide_ul.innerHTML = "";

                    for (let key of data) {
                        let li = document.createElement("li");
                        let categories = "";
                        let iterations = key.categories.length;

                        for (let category of key.categories) {
                            if (!--iterations) {
                                categories += category.name;
                            } else {
                                categories += category.name + ", ";
                            }
                        }
                        if (kind == 1) {
                            li.innerHTML = `
                              <div class="col">
                              <div class="title">Fundacja "${key.name}"</div>
                              <div class="subtitle">Cel i misja: ${truncate(
                                  key.description
                              )}
                              </div>
                              </div>

                              <div class="col"><div class="text">
                                ${categories}
                              </div></div>`;
                        } else if (kind == 2) {
                            li.innerHTML = `<div class="col">
                              <div class="title">Organizacja "${key.name}"</div>
                              <div class="subtitle">Cel i misja: ${truncate(
                                  key.description
                              )}</div>
                              </div>

                              <div class="col"><div class="text">
                                ${categories}
                              </div></div>`;
                        } else {
                            li.innerHTML = `<div class="col">
                              <div class="title">Lokalna zbiórka "${
                                  key.name
                              }"</div>
                              <div class="subtitle">Cel i misja: ${truncate(
                                  key.description
                              )}</div>
                              </div>

                              <div class="col"><div class="text">
                                ${categories}
                              </div></div>`;
                        }
                        current_slide_ul.appendChild(li);

                        document
                            .querySelectorAll("div.help--slides.active a.btn")
                            .forEach((a) => {
                                a.classList.remove("active");

                                if (a.dataset.page == page) {
                                    a.classList.add("active");
                                }
                            });
                    }
                },
                error: function () {},
            });
        }
    }
    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", (e) => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }
    document.querySelectorAll(".form-group--dropdown select").forEach((el) => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (
            tagName === "LI" &&
            target.parentElement.parentElement.classList.contains("dropdown")
        ) {
            return false;
        }

        if (
            tagName === "DIV" &&
            target.parentElement.classList.contains("dropdown")
        ) {
            return false;
        }

        document
            .querySelectorAll(".form-group--dropdown .dropdown")
            .forEach((el) => {
                el.classList.remove("selecting");
            });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(
                ".form--steps-instructions p"
            );
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.checked_categories = [];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach((btn) => {
                btn.addEventListener("click", (e) => {
                    e.preventDefault();

                    // Custom validation rules
                    jQuery.validator.addMethod("onlyDigits", function (
                        value,
                        element
                    ) {
                        return this.optional(element) || /^[0-9]*$/.test(value);
                    });
                    jQuery.validator.addMethod("zipcode", function (
                        value,
                        element
                    ) {
                        return (
                            this.optional(element) ||
                            /[0-9]{2}\-[0-9]{3}/.test(value)
                        );
                    });
                    jQuery.validator.addMethod("phoneNumber", function (
                        value,
                        element
                    ) {
                        if (
                            /(^|\W)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)/.test(
                                value
                            )
                        ) {
                            return true;
                        } else {
                            return false;
                        }
                    });
                    jQuery.validator.addMethod("date", function (
                        value,
                        element
                    ) {
                        if (
                            /^((0|1)\d{1})-((0|1|2)\d{1})-((19|20)\d{2})/.test(
                                value
                            )
                        ) {
                            return false;
                        } else {
                            return true;
                        }
                    });
                    jQuery.validator.addMethod("time24", function (
                        value,
                        element
                    ) {
                        if (
                            /^((0|1)\d{1})-((0|1|2)\d{1})-((19|20)\d{2})/.test(
                                value
                            )
                        ) {
                            return false;
                        } else {
                            return true;
                        }
                    });

                    // Validation
                    var form = $("form");
                    form.validate({
                        rules: {
                            bags: {
                                number: true,
                                min: 1,
                                max: 100,
                                onlyDigits: true,
                                required: true,
                            },
                            address: "required",
                            postcode: {
                                required: true,
                                zipcode: true,
                            },
                            address: "required",
                            city: "required",
                            phone: {
                                required: true,
                                phoneNumber: true,
                            },
                            data: {
                                required: true,
                                date: true,
                            },
                            time: {
                                required: true,
                                time24: true,
                            },
                        },
                        messages: {
                            bags: {
                                number: "Prosze wpisac liczbę",
                                min: "Minimum 1",
                                max: "Max 100",
                                onlyDigits:
                                    "Prosze wprowadzić liczbę całkowitą",
                                required: "Prosze wpisac liczbę",
                            },
                            address: "Pole jest wymagane",
                            postcode: {
                                required: "Pole jest wymagane",
                                zipcode: "Prosze wpisac poprawny kod",
                            },
                            city: "Pole jest wymagane",
                            phone: {
                                required: "Pole jest wymagane",
                                phoneNumber: "Prosze wprowadzic poprawny numer",
                            },
                            data: {
                                required: "Pole jest wymagane",
                                date: "Prosze wprowadzic poprawna date",
                            },
                            time: {
                                required: "Pole jest wymagane",
                                time24: "Prosze wprowadzic poprawna godzine",
                            },
                        },
                        errorElement: "div",
                    });

                    if (
                        this.currentStep == 3 &&
                        this.$form.querySelector(
                            "input[name=organization]:checked"
                        ) !== null
                    ) {
                        this.currentStep++;
                        this.updateForm();
                    } else if (
                        form.valid() == true &&
                        this.$form.querySelectorAll(
                            "input[name=categories]:checked"
                        ).length &&
                        this.currentStep != 3
                    ) {
                        this.currentStep++;
                        this.updateForm();
                    }
                });
            });

            // Previous step
            this.$prev.forEach((btn) => {
                btn.addEventListener("click", (e) => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form
                .querySelector("form")
                .addEventListener("submit", (e) => this.submit(e));

            // 1 Step next
            this.$form
                .querySelector(
                    "div:nth-child(1) > div.form-group.form-group--buttons > button"
                )
                .addEventListener("click", (e) => {
                    this.checked_categories = [];
                    this.$form
                        .querySelectorAll("input[name=categories]:checked")
                        .forEach((checked) => {
                            this.checked_categories.push(
                                parseInt(checked.value)
                            );
                        });

                    this.getInstitution();
                });
        }

        validation() {}

        /**
         * Get institutions filtered by selected categories
         */
        getInstitution() {
            $.ajax({
                type: "GET",
                url: "/institutions/",
                data: { category: this.checked_categories },
                traditional: true,
                success: function (data) {
                    let div = form.querySelector('div[data-step="3"]');
                    div.querySelectorAll(
                        'div[class="form-group form-group--checkbox"]'
                    ).forEach((div) => {
                        div.remove();
                    });

                    for (let key of data) {
                        div.children[0].insertAdjacentHTML(
                            "afterend",
                            `<div class="form-group form-group--checkbox">
                              <label>
                                <input type="radio" name="organization" value="${key.id}">
                                <span class="checkbox radio"></span>
                                <span class="description">
                                  <div class="title">Fundacja “${key.name}”</div>
                                  <div class="subtitle">
                                    Cel i misja: ${key.description}
                                  </div>
                                </span>
                              </label>
                            </div>`
                        );
                    }
                },
            });
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */

        updateForm() {
            this.$step.innerText = this.currentStep;

            this.slides.forEach((slide) => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden =
                this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // Get data from inputs and show them in summary

            if (this.currentStep == 5) {
                let div = form.querySelector('div[data-step="5"]');

                let bags = form.querySelector('input[name="bags"]').value;
                let institution = form.querySelector(
                    'input[type="radio"]:checked'
                ).nextElementSibling.nextElementSibling.children[0].textContent;
                let address = form.querySelector('input[name="address"]').value;
                let city = form.querySelector('input[name="city"]').value;
                let postcode = form.querySelector('input[name="postcode"]')
                    .value;
                let phone = form.querySelector('input[name="phone"]').value;
                let data = form.querySelector('input[name="data"]').value;
                let time = form.querySelector('input[name="time"]').value;
                let more_info = form.querySelector('textarea[name="more_info"]')
                    .value;

                function variety(amount, singular, plural, plural_genetive) {
                    if (amount == 1) return singular;
                    var rest10 = amount % 10;
                    var rest100 = amount % 100;
                    if (
                        rest10 > 4 ||
                        rest10 < 2 ||
                        (rest100 < 15 && rest100 > 11)
                    )
                        return plural_genetive;
                    return plural;
                }

                form.querySelector(
                    'span[class="icon icon-bag"]'
                ).nextElementSibling.innerHTML = `${bags} ${variety(
                    bags,
                    "Worek",
                    "Worki",
                    "Worków"
                )}`;
                form.querySelector(
                    'span[class="icon icon-hand"]'
                ).nextElementSibling.innerHTML = `Dla fundacji ${institution.substring(
                    9
                )}`;

                let section_columns = div.querySelector(
                    "div.form-section--columns"
                );

                section_columns.children[0].children[1].innerHTML = `
                  <li>${address}</li>
                  <li>${city}</li>
                  <li>${postcode}</li>
                  <li>${phone}</li>
                  `;
                section_columns.children[1].children[1].innerHTML = `
                  <li>${data}</li>
                  <li>${time}</li>
                  <li>${more_info}</li>
                  `;
            }
        }

        /**
         * Submit form
         * Send data to server
         */
        submit(e) {
            e.preventDefault();

            $.ajax({
                type: "POST",
                url: "/add-donation/",
                traditional: true,
                data: {
                    quantity: form.querySelector('input[name="bags"]').value,
                    categories: this.checked_categories,
                    institution: form.querySelector(
                        'input[type="radio"]:checked'
                    ).value,
                    address: form.querySelector('input[name="address"]').value,
                    city: form.querySelector('input[name="city"]').value,
                    zip_code: form.querySelector('input[name="postcode"]')
                        .value,
                    phone_number: form.querySelector('input[name="phone"]')
                        .value,
                    pick_up_date: form.querySelector('input[name="data"]')
                        .value,
                    pick_up_time: form.querySelector('input[name="time"]')
                        .value,
                    pick_up_comment: form.querySelector(
                        'textarea[name="more_info"]'
                    ).value,
                    csrfmiddlewaretoken: Cookies.get("csrftoken"),
                },
                success: function (data) {
                    document.location.href = "/form-confirmation/";
                },
                error: function (data) {
                    console.log(data);
                    let message = `Error [${data["status"]}]:\n`;
                    for (let key in data["responseJSON"]) {
                        message +=
                            data["responseJSON"][key][0]["message"] + "\n";
                    }
                    alert(message);
                },
            });
        }
    }
    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
