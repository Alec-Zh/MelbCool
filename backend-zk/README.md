首次初始化数据库
pnpm prisma:generate

启动
pnpm dev

修改单个
pnpm prisma:studio 

删除所有
node ./scripts/deleteAllData.js  (mac)   node .\scripts\deleteAllData.js  (windows) 

导入所有数据
node ./scripts/importData.js   (mac)     node .\scripts\importData.js    (windows)
