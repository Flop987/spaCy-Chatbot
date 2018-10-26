import spacy
import wikipedia
nlp = spacy.load('en_core_web_sm')

def tag():
    subject = ""

    for t in user_doc:
        print (t.text,t.pos_,t.tag_,t.dep_,t.head.text,t.head.dep_)
        if t.tag_ == "WRB":
            question_type = t.text.lower()
        elif t.tag_ == "WP":
            question_type = t.text.lower()
        elif t.dep_ in ("nsubj" ,"nsubjpass" ,"attr", "dobj"):
            if t.dep_ == "det":
                if any(i.isupper() for i in t.text):
                #checks for capital letter in t.text
                    subject += " " + t.text.lower()
            else:
                subject += " " + t.text.lower()

        elif t.head.dep_ in ("nsubj" ,"nsubjpass" ,"attr", "dobj"):
            if t.dep_ == "det":
                if any(i.isupper() for i in t.text):
                    subject += " " + t.text.lower()
            else:
                subject += " " + t.text.lower()
        elif t.dep_ == "ROOT":
            detail = t.text.lower()
    if subject != "" and question_type != "" and detail !="":
        print ("\nquestion type is " + question_type)
        print ("subject is" + subject)
        print ("detail is " + detail)
        return (question_type,subject,detail)
    else:
        print ("That's not a question I can answer.")
def response():
    search = wikipedia.search(subject)
    if search == []:
        print ("Sorry no page found")
    summary = wikipedia.summary(subject)
    # print (summary)
    summary_doc = nlp(summary)
    sentences = summary_doc.sents
    answers = []
    if question_type == "who":
        if detail == "is":
            answers.append(wikipedia.summary(subject,sentences = 1))
        else:
            for sents in sentences:
                # print ("A")
                for w in sents:
                    # print ("B")
                    doc = nlp(w.text)
                    ents = doc.ents
                    for e in ents:
                        # print ("C")
                        if e.label_ == "PERSON" and w.text != subject:
                            answers.append(sents)
                            # print("PErson found")
                            break
                    else:
                        continue
                    break
                if len(answers) > 3:
                    break
        return answers
                    # else:
                    #     continue
                    # break
                # else:
                #     continue
                # break
    if question_type == "what":
        if detail == "is":
            answers.append(wikipedia.summary(subject,sentences = 1))
        else:
            for sents in sentences:
                for w in sents:
                    if w.text == subject:
                        answers.append(sents)
                        break
                    else:
                        continue
                    break
                if len(answers) > 3:
                    break
        return answers
    if question_type == "when":
        for sents in sentences:
            # print (sents)
            for w in sents:
                # print (w.text)
                doc = nlp(w.text)
                ents = doc.ents
                for e in ents:
                    if e.label_ == "DATE":
                        answers.append(sents)
                        break
                else:
                    continue
                break
            if len(answers) > 3:
                break
        return answers

    if question_type == "why":
        for sents in sentences:
            for w in sents:
                if w.text in (detail, "because", "due to","as a result","reason"):
                    answers.append(sents)
                    break
            if len(answers) > 3:
                break
        return answers
    if question_type == "where":
        for sents in sentences:
            for w in sents:
                doc = nlp(w.text)
                ents = doc.ents
                for e in ents:
                    if e.label_ == "GPE" or e.label_ == "LOC":
                        answers.append(sents)
                        break
                else:
                    continue
                break
            if len(answers) > 3:
                break
        return answers

    if question_type == "how":
        for sents in sentences:
            for w in sents:
                if w.text in ("by","using",detail):
                    answers.append(sents)
                    break
            if len(answers) > 3:
                break
        return answers
def write():
    file = open("Recorded Answers","a+")
    file.write("\n"+ user_input)
    file.write("\n"+ best_ans)

while True:
    user_input = input('Type quit to exit\nAsk me something!: ')
    user_doc = nlp(user_input)
    if user_input == "quit":
        exit()
    question_type,subject,detail = tag()
    response()
    answers = response()
    count = 1
    for a in answers:
        print ( "\n"+ str(count) + ")")
        print (a)
        count +=1
    if len(answers) >1:
        answer_input = int(input('Which answer was the most accurate?\nType in the answer number: '))
        best_ans = str(answers[answer_input - 1])
        print (best_ans)
        write()
