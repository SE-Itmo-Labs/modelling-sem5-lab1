#import "template/report.typ": lab-report
#import "config.typ": config
#import "sections/task.typ": task
#import "sections/work.typ": work
#import "sections/conclusion.typ": conclusion

#lab-report(
  config: config,
  task: task,
  work: work,
  conclusion: conclusion,
)
