import xlrd
import json
import sys
import argparse

def buildTeamsFromFile(filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)

    org_chart = {}
    uid_to_name = {}
    lead = None

    for r in range(1,sheet.nrows):
        row = sheet.row(r)

        uid = row[0].value
        name = row[1].value
        boss = row[2].value


        uid_to_name[uid] = name
        if boss == "":
            lead = uid
            org_chart[uid] = []
        else:
            if boss not in org_chart:
                org = [uid]
            else:
                org = org_chart[boss]
                org.append(uid)
            org_chart[boss] = org

    return org_chart, uid_to_name, lead


def buildOrgFromTeams(lead, converter, teams):
    if lead not in teams:
        return { "name" : converter[lead] }

    org_chart = {
        "name" : converter[lead]
    }

    children = []
    for child in teams[lead]:
        children.append(buildOrgFromTeams(child, converter, teams))

    org_chart["children"] = children

    return org_chart


def handleArgs(argv):
    description = "Converts Workday-generated orgchart xls file into JSON."
    parser = argparse.ArgumentParser(description)
    parser.add_argument("--input", "-i", help="Input file name (xls format)", default="report.xls")
    parser.add_argument("--output", "-o", help="Output file name (json format)", default="orgchart.json")

    args = parser.parse_args()
    return args.input, args.output;


def main(argv):
    input_file, output_file = handleArgs(argv)
    teams, conv, lead = buildTeamsFromFile(input_file)
    print("Lead: %s\n%r" % (conv[lead], teams))
    print("\n\n\n")
    oc = buildOrgFromTeams(lead, conv, teams)
    print(oc)

    with open(output_file, 'w') as outfile:
        json.dump(oc, outfile)


if __name__ == "__main__":
    main(sys.argv[1:])


