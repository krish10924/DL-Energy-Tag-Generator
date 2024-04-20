// Global Variables
var CUTOFF = 0.5
var QUESTION_BODY_CLASSNAME =  'post-layout'
var TAGS_CLASSNAME = "ml0 list-ls-none js-post-tag-list-wrapper d-inline"


var body = JSON.stringify(
    document
    .getElementsByClassName('s-prose js-post-body')[0]
    .innerHTML)
    .replace(/\s\s+/g, ' ') 

var title = document.getElementById('question-header').getElementsByTagName('h1')[0].innerText
var DLTags = ['tensorflow', 'keras', 'caffe', 'theano', 'pytorch', 'gpu', 'cuda', 'tensorflow-lite', 'tensorflow-federated']

var requestURL = "http://localhost:8500/"
var requestBody = {
    "title": title, 
    "body": body
    }

// Function to verify tags by deep learning posts. 
function checkIfDL() {
    const tagElements = document.querySelectorAll('.post-taglist .post-tag');
    const tags = Array.from(tagElements).map(tagElement => tagElement.textContent.trim());
    
    for(let tag in tags){
        if(DLTags.includes(tags[tag])){
            return true;        }
    }
    return false
}

function getPatternURLOffset(tagname){
    switch(tagname){
        case 'checkpoint': return 'checkpoint.html';
        case 'quantization': return 'quantization.html'; 
        case 'efficient read write': return 'read-write.html';
        case 'memory leaks': return 'leaks.html'; 
        case 'pretrained networks': return 'pretrained.html';
        case 'tensor operations': return 'tensor.html';
        default: return 'tensor.html';
    }
}

function generateTag(tagname){
    e = document.createElement('div')
    a = document.createElement('a')
    e.className = 'energytag'
    e.innerText = tagname
    a.target = '_blank'
    a.href = chrome.runtime.getURL('pages/index.html');
    //a.href = 'pages/index.html';
    a.appendChild(e)
    return a
}

function prependTagToQuestion(e){
    document.getElementsByClassName(QUESTION_BODY_CLASSNAME)[0].prepend(e)
}

function tagQuestion(res){
    if (res.pattern){
            tagElement = generateTag(res.pattern)
            prependTagToQuestion(tagElement)
        }
    
}

if(checkIfDL()){
    var xhr = new XMLHttpRequest();  
    xhr.open("POST", requestURL);  
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() { 
      if (xhr.readyState == 4)
        if (xhr.status == 200){
            res = JSON.parse(xhr.responseText)
            tagQuestion(res)
        }
    };

    xhr.send(JSON.stringify(requestBody)); 
}
