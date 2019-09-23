from httprunner.api import HttpRunner
from httprunner.api import report
runner = HttpRunner()
runner.run("testsuites/parameters_creat_user.yml")
report.render_html_report(32)
summary = runner.summary

print(summary)

