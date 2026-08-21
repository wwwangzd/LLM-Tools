# 基于条件的等待

异步测试应等待真实状态，而不是猜测操作需要多长时间。

## 判断原则

以下情况优先使用条件等待：

- 测试包含没有业务含义的 `sleep` 或 `setTimeout`。
- 测试本地通过，但在 CI、并行运行或高负载下偶发失败。
- 测试等待事件、状态、数量或文件出现。

只有测试目标本身就是时间行为，例如防抖、节流或固定周期，才使用固定延迟；此时先等待触发条件，并注释说明延迟值的业务依据。

## 基本模式

不要这样做：

```typescript
await new Promise(resolve => setTimeout(resolve, 500));
expect(getResult()).toBeDefined();
```

改为等待目标条件：

```typescript
await waitFor(
  () => getResult(),
  'result to become available'
);
```

## 通用实现

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise(resolve => setTimeout(resolve, 10));
  }
}
```

完整的领域化示例位于
[`../examples/condition-based-waiting-example.ts`](../examples/condition-based-waiting-example.ts)。

## 实现要求

- 每次轮询都重新读取状态，避免使用循环外缓存的旧数据。
- 必须设置总超时，并让错误信息描述等待的条件和已观察到的状态。
- 采用合理轮询间隔，避免无意义地占用 CPU。
- 优先复用项目测试框架已有的 `waitFor`、事件订阅或异步断言。
- 如果能够订阅确定事件，优先事件通知；轮询用于没有可靠通知机制的场景。

## 固定延迟确实合理时

```typescript
await waitForEvent(manager, 'TOOL_STARTED');
await new Promise(resolve => setTimeout(resolve, 200));
// 被测工具每 100ms 输出一次；等待 200ms 用于验证两个周期。
```

固定延迟必须同时满足：

1. 已先等待触发条件。
2. 延迟基于明确的业务时序，而不是经验猜测。
3. 测试中记录选择该数值的原因。
