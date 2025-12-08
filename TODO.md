# TODO: Implement Question Pagination for Exam Taking

- [x] Update main/urls.py to include question_index parameter in take_exam URL pattern
- [x] Modify main/views.py take_exam function to handle question pagination, session storage for answers, and conditional submission
- [x] Update main/templates/take_exam.html to display one question per page with Next, Previous, and Submit buttons at bottom right
- [ ] Test the exam flow for correct navigation and submission
- [ ] Verify timer functionality across pages
