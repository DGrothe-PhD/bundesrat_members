from html.parser import HTMLParser
import json

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.state = "init"
        self.stack = []
        self.parsed_data = {}
        self.all_data = []
        self.init_parsed_data()

    def init_parsed_data(self):
        self.parsed_data = {
            "gender": "?"
        }

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)
        html_class_tag = [ x[1] for x in attrs if x[0] == "class"]
        if len(html_class_tag) > 0:
            html_classes = [ x.strip() for x in html_class_tag[0].split(" ")]
        else:
            html_classes = []
        if self.state == "init" and ("vcard" in html_classes):
            self.state = "vcard"
            print("entered vcard")
        elif self.state == "vcard" and ("members-details" in html_classes):
            self.state = "members-details"
        elif self.state == "members-details" and tag == "h2":
            self.state = "member-name"
        elif self.state == "member-details" and ("organization-name" in html_classes):
            self.state = "org-name"
        elif self.state == "member-details" and ("state" in html_classes):
            self.state = "state_name"
        elif self.state == "member-details" and ("vcard" in html_classes):
            self.state = "real_vcard"
        elif self.state == "real_vcard" and tag == "strong":
            self.state = "role"
        elif self.state == "real_vcard" and ("email" in html_classes) and tag == "p":
            self.state = "email"
        elif self.state == "real_vcard" and ("street-address" in html_classes):
            self.state = "street"
        elif self.state == "real_vcard" and ("postal-code" in html_classes):
            self.state = "postal"
        elif self.state == "real_vcard" and ("tel" in html_classes):
            self.state = "tel_number"
        elif self.state == "tel_number" and ("type" in html_classes):
            self.state = "tel_type"
        elif self.state == "tel_pre_fax" and ("value" in html_classes):
            self.state = "tel_fax"
        elif self.state == "tel_pre_phone" and ("value" in html_classes):
            self.state = "tel_phone"
        if self.state != "init":
            self.stack.append(tag)
        print(self.state)

    def handle_endtag(self, tag):
        if len(self.stack) > 0:
            self.stack.pop()
        print("stack: ", len(self.stack))
        if len(self.stack) == 0 and self.state != "init":
            self.state = "init"
            print("entered init")
            print(self.parsed_data)
            self.all_data.append(self.parsed_data)
            self.init_parsed_data()
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if len(self.stack) > 0:
            current_tag = self.stack[-1]
        else:
            current_tag = "foobar"
        if self.state == "org-name":
            self.parsed_data['party'] = data.strip()
            self.state = "member-details"
        elif self.state == "member-name" and current_tag == "a":
            self.parsed_data['name'] = data.replace("|", "").strip()
            self.state = "member-details"
        elif self.state == "state_name":
            self.parsed_data['state'] = data.strip()
            self.state = "member-details"
        elif self.state == "role":
            self.parsed_data['role'] = data.strip()
            self.state = "real_vcard"
        elif self.state == "email" and current_tag == "a":
            self.parsed_data['email'] = data.strip()
            self.state = "real_vcard"
        elif self.state == "street":
            self.parsed_data['street'] = data.strip()
            self.state = "real_vcard"
        elif self.state == "postal":
            self.parsed_data['postal_code'] = data.strip()
            self.state = "real_vcard"
        elif self.state == "tel_type":
            d = data.strip()
            if d == "fax":
                self.state = "tel_pre_fax"
            else:
                self.state = "tel_pre_phone"
        elif self.state == "tel_fax":
            self.parsed_data['fax'] = data.strip()
            self.state = "real_vcard"
        elif self.state == "tel_phone":
            self.parsed_data['phone'] = data.strip()
            self.state = "real_vcard"
        print("Encountered some data  :", data)


with open("mitglieder.html") as f:
    content = f.read()
parser = MyHTMLParser()
parser.feed(content)
with open("bundesrat.json", "w+") as f:
    f.write(json.dumps(parser.all_data))
