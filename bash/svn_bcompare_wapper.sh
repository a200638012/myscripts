#!/bin/bash
# SVN参数转BCompare可接受格式的包装脚本（精简版，无冗余echo）

# 初始化文件路径数组
file_paths=()

# 遍历处理参数（从索引1开始，跳过脚本自身）
i=1
while [ $i -le $# ]; do
    current_arg="${!i}"

    # 过滤SVN的-u参数
    if [ "$current_arg" = "-u" ]; then
        i=$((i + 1))
        continue
    fi

    # 过滤SVN的-L参数及对应的标签
    if [ "$current_arg" = "-L" ] && [ $((i+1)) -le $# ]; then
        i=$((i + 2))
        continue
    fi

    # 收集有效文件路径
    if [ -f "$current_arg" ]; then
        file_paths+=("$current_arg")
    fi

    i=$((i + 1))
done

# 调用BCompare（仅保留错误提示）
if [ ${#file_paths[@]} -ge 2 ]; then
    /your_bcompare_path "${file_paths[0]}" "${file_paths[1]}"
else
    echo "❌ 错误：未提取到足够的文件路径（需2个，实际${#file_paths[@]}个），无法执行BCompare"
    exit 1
fi