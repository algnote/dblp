# dblp

## 参数说明

n1: 最少在该会议发过n1篇论文才算该会议的支持者

n2, n3: 最少最近n2年在该会议发过n3篇文章才算活跃

n4: 在11年最少合作过n4次才算做团体

n5: 在前5年最少合作过n5次才算是团体

n6: 在后六年最少合作过n6次才算是团体

## 输出说明

suport.json: 各个会议的支持者

active.json: 依然活跃者

no_active.json: 不再活跃者

groups: 团体

co_auths.json: 团体的详细数据，[团队1，[[conference id，year id, title, 序号]，[团队1， conference id，year id, title, 序号]]]

co_auths_pre.json: 前5年团体的详细数据，格式同上

co_auths_post.json: 后6年团体的详细数据，格式同上