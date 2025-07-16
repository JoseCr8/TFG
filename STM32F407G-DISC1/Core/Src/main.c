/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stdio.h"
#include "DHT.h"
#include "MAX31865.h"
#include "LIS3DSH.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
//#define DHT11_PORT GPIOC
//#define DHT11_PIN GPIO_PIN_9

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
//HC-SR04
uint8_t txData[30];
uint8_t rxData[2];

uint32_t echo1, echo2, delay_hcsr04;
float dist1, dist2;
//PT100
Max31865_t  pt100;
bool        pt100isOK;
float       pt100Temp;
uint8_t fault;
uint16_t rtd_raw;

//ACCELEROMETER
LIS3DSH_DataScaled current_acceleration;

//DHT11
//uint8_t Rh_byte1, Rh_byte2, Temp_byte1, Temp_byte2;
//uint16_t SUM, RH, TEMP;

DHT_DataTypedef DHT11_Data;
float Temperature = 0;
float Humidity = 0;
uint32_t delay_dht11;
//uint8_t Presence = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
/*
void delay (uint16_t time){
	__HAL_TIM_SET_COUNTER(&htim6, 0);
	while ((__HAL_TIM_GET_COUNTER(&htim6)) < time);
}

void set_pin_output (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin){
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void set_pin_input (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin){
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void DHT11_Start (void){
	set_pin_output(DHT11_PORT, DHT11_PIN);
	HAL_GPIO_WritePin(DHT11_PORT, DHT11_PIN, 0); //pull the pin low
	delay(18000);
	HAL_GPIO_WritePin(DHT11_PORT, DHT11_PIN, 1); //pull the pin high
	delay(20);
	set_pin_input(DHT11_PORT, DHT11_PIN);
}

uint8_t DHT11_Check_Response (void){
	uint8_t Response = 0;
	delay(40);
	if (!(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN)))
	{
		delay(80);
		if((HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN))) Response = 1;
		else Response = -1;
	}
	uint32_t time1 = HAL_GetTick();
	while (HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && (HAL_GetTick() - time1) < 20); // wait for the pin to go low

	return Response;
}

uint8_t DHT11_Read (void){
	uint8_t i,j;
	for (j = 0; j < 8; j++)
	{
		while (!(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN))); // wait for the pin to go high
		delay(40);
		if (!(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN))) // if the pin is low
		{
			i&= ~(1<<(7-j)); // write 0
		}
		else i|= (1<<(7-j)); // if the pin is high write 1
		uint32_t time2 = HAL_GetTick();
		while (HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && (HAL_GetTick() - time2) < 50); // wait for the ping to go low
	}
	return i;
}
*/
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */
  LIS3DSH_InitTypeDef accelerometerConfig;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM8_Init();
  MX_TIM11_Init();
  MX_USART2_UART_Init();
  MX_SPI2_Init();
  MX_SPI1_Init();
  /* USER CODE BEGIN 2 */
  //HAL_TIM_Base_Start(&htim6);
  HAL_TIM_Base_Start(&htim11);
  HAL_TIM_Base_Start(&htim11);
  HAL_TIM_PWM_Start(&htim11, TIM_CHANNEL_1);
  HAL_TIM_IC_Start(&htim8, TIM_CHANNEL_1);
  HAL_TIM_IC_Start(&htim8, TIM_CHANNEL_2);
  TIM11->CCR1 = 3;

  Max31865_init(&pt100,&hspi2,GPIOC,GPIO_PIN_8,3,50);

  accelerometerConfig.dataRate = LIS3DSH_DATARATE_12_5;
  accelerometerConfig.fullScale = LIS3DSH_FULLSCALE_4;
  accelerometerConfig.antiAliasingBW = LIS3DSH_FILTER_BW_50;
  accelerometerConfig.enableAxes = LIS3DSH_XYZ_ENABLE;
  accelerometerConfig.interruptEnable = false;
  LIS3DSH_Init(&hspi1, &accelerometerConfig);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	// DISTANCE SENSORS
	HAL_GPIO_TogglePin(BlueLed_GPIO_Port, BlueLed_Pin);
	if (HAL_GetTick() - delay_hcsr04 >= 100){ // every 100 ms
		delay_hcsr04 = HAL_GetTick();
		echo1 = HAL_TIM_ReadCapturedValue(&htim8, TIM_CHANNEL_1);
		echo2 = HAL_TIM_ReadCapturedValue(&htim8, TIM_CHANNEL_2);
		dist1 = echo1 / 58.0f;
		dist2 = echo2 / 58.0f;
	}

	float t;
	HAL_GPIO_TogglePin(GreenLed_GPIO_Port, GreenLed_Pin);

	// PT100 temperature sensor
	pt100isOK = Max31865_readTempC(&pt100,&t);
	rtd_raw = Max31865_readRTD(&pt100);
	if (pt100isOK != false){
		pt100Temp = Max31865_Filter(t,pt100Temp,0.1);
	}
	else{
		fault = Max31865_readFault(&pt100);
	}

	if (LIS3DSH_PollDRDY(100)) {
		current_acceleration = LIS3DSH_GetDataScaled();
		current_acceleration.x;
		current_acceleration.y;
		current_acceleration.z;
	}

	snprintf((char*)txData, sizeof(txData), "%.2f,%.2f,%.2f\r\n", dist1,dist2,pt100Temp);
	HAL_UART_Transmit(&huart2, txData, sizeof(txData), 100);
	HAL_UART_Receive(&huart2, rxData, sizeof(rxData), 100);
	HAL_GPIO_TogglePin(OrangeLed_GPIO_Port, OrangeLed_Pin);
	HAL_Delay(100);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 160;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV4;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
