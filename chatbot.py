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
    if question_type == "who" or question_type == "what":
        if detail == "is":
            print (wikipedia.summary(subject,sentences = 1))
        else:
            for sents in sentences:
                for w in sents:
                    doc = nlp(w.text)
                    ents = doc.ents
                    for e in ents:
                        if e.label_ == "PERSON":
                            print (sents)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

    if question_type == "when":
        for sents in sentences:
            # print (sents)
            for w in sents:
                # print (w.text)
                doc = nlp(w.text)
                ents = doc.ents
                for e in ents:
                    if e.label_ == "DATE":
                        print (sents)
                        break
                else:
                    continue
                break
            else:
                continue
            break

    if question_type == "why":
        for sents in sentences:
            for w in sents:
                if w.text in (detail, "because", "due to","as a result","reason"):
                    print(sents)
                    break
            else:
                continue
            break

    if question_type == "where":
        for sents in sentences:
            for w in sents:
                doc = nlp(w.text)
                ents = doc.ents
                for e in ents:
                    if e.label_ == "GPE" or e.label_ == "LOC":
                        print (sents)
                        break
                else:
                    continue
                break
            else:
                continue
            break

    if question_type == "how":
        for sents in sentences:
            for w in sents:
                if w.text in ("by","using",detail):
                    print (sents)
                    break
            else:
                continue
            break

while True:
    user_input = input('Type quit to exit\nAsk me something!: ')
    user_doc = nlp(user_input)
    if user_input == "quit":
        exit()
    question_type,subject,detail = tag()
    response()
