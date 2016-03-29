/**
    questions standsrt output template usage

    i realy have to take a look how to translate
    @variable rithtAnswersAmount and
    @variable questionNumber inside template functions
    without creating variables outside
    some reasons questionType cant be pasted directly in
    template json
*/
function questionType( rightAnswersAmount ){
    return rightAnswersAmount == 1 ? "radio" : "checkbox" ;
}
var questionNumber;
var rightAnswersAmount;
    var questionInfo = {
        'question': {
                html: function(target) {
                    questionNumber = target.index;
                    rightAnswersAmount = this.options.reduce((a, b) => a + b.right, 0);
                    return this.text; }
                },
        'options': {
            'option-container': {
                    'class': function() { return questionType(rightAnswersAmount) }
            },
            'input': {
                    type: function() { return questionType(rightAnswersAmount) },
                    value: function() { return this.right ? 1 : 0 },
                    name: function() { return currentTheme + questionNumber }
            },
            'content': {
                    html: function() { return this.text }
            }
        },
        'help-button': {
                'data-target': function() { return "#help-" + questionNumber }
        },
        'help': {
                id: function() { return "help-" + questionNumber },
                'name': {
                        html: function() { return this.name; }
                },
                'content': {
                        html: function() { return this.content; }
                }
        }
    }

//$('#question-template').render(questions, questionInfo);

/**
    here is some stupido functions to check question by clicking
        and show small statistics
*/
var right = 0;
var wrong = 0;

var wrongProgress = document.getElementById('wrong-progress');
var rightProgress = document.getElementById('right-progress');
var total = document.getElementsByClassName('question').length;

function showProgress(){
    document.getElementById('progress');
    rightProgress.style.width = (right / total) * 100 + '%';
    rightProgress.innerHTML = '';
    wrongProgress.style.width = (wrong / total) * 100 + '%';
    wrongProgress.innerHTML = '';
}

function checkInput(input){
    var optionContainer = input.closest("label");
        input.disabled = true;
    if (input.value == 0){
            input.checked = false;
            optionContainer.classList.add('text-danger');
        optionContainer.classList.add('disabled');
    } else {
        optionContainer.classList.add('text-success');
    }
}
function isAnswered(questionContainer){
    return questionContainer.classList.contains('panel-success') || questionContainer.classList.contains('panel-danger');
}
function checkChoosenInputs(element){
    var pass = true;
    var questionContainer = element.closest('.panel-default');
    [].forEach.call(element.getElementsByTagName('label'), function(subelement){
        var input = subelement.getElementsByTagName('input')[0];
        var optionContainer = subelement.closest("li");
        if ((input.value == 0 && input.checked)
                || (input.value == 1 && !input.checked)){
                pass = false;
                if (input.checked) {
                    checkInput(input);
                }
            }
    });
    if (pass) {
        if (!isAnswered(questionContainer)){
                questionContainer.classList.add('panel-success');
                questionContainer.getElementsByClassName('answer')[0].classList.add('disabled');
                right += 1;
            }
            [].forEach.call(element.getElementsByTagName('input'), function(input){
                checkInput(input);
            });
    } else {
            [].forEach.call(element.getElementsByTagName('input'), function(input){
                input.checked = false;
            });
            if (!isAnswered(questionContainer)){
            questionContainer.classList.add('panel-danger');
            wrong += 1;
        }
    }
    showProgress();
}

    function bindButtons(){
    [].forEach.call(document.getElementsByClassName('answer'), function(button){
        button.onclick = function() {
            checkChoosenInputs(this.closest(".options-container"));
        }
    });
}

/**
    menu builder
*/
function renderList(list, array, clickHandler){
    list.innerHTML = "";
    [].forEach.call(array, function(theme){
        var themeSelector = document.createElement('li');
        var themeA = document.createElement('a');
        themeA.href = "#";
        themeA.onclick = function() {
            [].forEach.call(list.getElementsByClassName('bg-danger'), function(liElement){
                liElement.classList.remove('bg-danger');
            });
            themeSelector.classList.add('bg-danger');
            clickHandler(theme) };
        themeA.innerHTML = theme['name'];
        themeSelector.appendChild(themeA);
        list.appendChild(themeSelector);
    });
  }

var currentTheme = 'Default';
function renderSys(data){
    var courseList = document.getElementById('course-selector').getElementsByClassName('dropdown-menu')[0];
    renderList(courseList, data, renderCourse);
}
function renderCourse(course){

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var course = JSON.parse(xmlhttp.responseText);
            var list = document.getElementById('theme-selector').getElementsByClassName('dropdown-menu')[0];
            document.getElementById('main-container').innerHTML = "";
            renderList(list, course['themes'], renderTheme);
            document.getElementById('course-name').innerHTML = course['name'].match(/\d+\.\d+/i);
        }
    }

    xmlhttp.open("GET", course['url'], true);
    xmlhttp.send();
}
function renderTheme(theme){

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            theme = JSON.parse(xmlhttp.responseText)

            currentTheme = theme['name'];
            var questionTemplate = document.getElementById('question-template');
            tst = questionTemplate.cloneNode(true);
            tst.id = 'questions-container';
            $(tst).detach();
            document.getElementById('main-container').innerHTML = "";
            tst.classList.remove('hidden');
            Transparency.render(tst, theme.questions, questionInfo);
            right = 0;
            wrong = 0;
            total = theme['questions'].length;
            document.getElementById('main-container').appendChild(tst);
            bindButtons();
            showProgress();
        }
    }

    xmlhttp.open("GET", theme['url'], true);
    xmlhttp.send();
}

var xmlhttp = new XMLHttpRequest();
var coursesUrl = "../api/courses/?format=json";

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var myArr = JSON.parse(xmlhttp.responseText);
        renderSys(myArr);
    }
};
xmlhttp.open("GET", coursesUrl, true);
xmlhttp.send();

//renderSys(data);