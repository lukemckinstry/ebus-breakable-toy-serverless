

aws ecs execute-command --region us-east-1 --cluster app --task <ENTER-TASK-ID-HERE> --container sun-api --command "/bin/bash" --interactive