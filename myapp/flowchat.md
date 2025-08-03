flowchart TD
  subgraph ClickUp Integration
    A[ClickUp User<br/>creates a Task] -->|webhook POST| B[  /Django populate-projectcreated/ ]
    B -->|creates/updates| C[(PostgreSQL Project/Task)]
  end

  subgraph Employee UI
    D[Employee Browser]<br/>“Squad Work Logger” Form
    D -->|GET /projects| E[Django projects view]
    E -->|renders| D
    D -->|POST /worklogs| F[Django worklog view]
    F -->|writes| G[(PostgreSQL WorkLog)]
  end

  subgraph Admin UI
    H[django.contrib.admin]
    H -->|list_filter & custom changelist| I[WorkLogAdmin]
    I -->|aggregates| G
    I -->|injects JS data| J[admin change_list.html + Chart.js]
    J -->|renders charts| H
  end

  subgraph Slack Reminder
    K[Schedule by Zapier<br/>(7pm & 2am)]
    K -->|GET /daily_missing_report| L[Django daily_missing_report view]
    L -->|returns JSON of missing employees| M[Zapier Loop]
    M -->|lookup Slack IDs| N[Google Sheet]
    N -->|for each missing| O[Slack “you’ve not logged” DM]
  end

  style ClickUp Integration fill:#f9f,stroke:#333,stroke-width:1px
  style Employee UI fill:#bbf,stroke:#333,stroke-width:1px
  style Admin UI fill:#bfb,stroke:#333,stroke-width:1px
  style Slack Reminder fill:#ffb,stroke:#333,stroke-width:1px
