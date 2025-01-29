import { Handler } from 'aws-lambda';
import { ethers } from 'ethers';
import { SwapPayload } from './types';

const provider = new ethers.providers.InfuraProvider('mainnet', process.env.INFURA_KEY);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

export const handler: Handler<SwapPayload> = async (event) => {
  try {
    const { action, asset, amount } = event;

    // Uniswap Router 配置
    const routerAddress = "0x7a250d3810FC4a479A6Df5C6B1A2F0A8B5a7eAe8";
    const routerABI = [
      "function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] path, address to, uint deadline)"
    ];
    const router = new ethers.Contract(routerAddress, routerABI, wallet);

    // 交易路径（示例：USDC → OUSG）
    const path = [
      "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
      "0x1B19C19393e2d034D8Ff31ff34c81252FcBbee92"  // OUSG
    ];

    const deadline = Math.floor(Date.now() / 1000) + 600; // 10分钟

    // 执行交易
    const tx = await router.swapExactTokensForTokens(
      ethers.utils.parseUnits(amount.toString(), 6), // USDC 精度为6
      0, // 最小输出
      path,
      wallet.address,
      deadline
    );

    await tx.wait();

    return {
      statusCode: 200,
      body: JSON.stringify({ txHash: tx.hash })
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Transaction failed" })
    };
  }
};