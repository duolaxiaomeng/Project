#include<stdio.h>
#include<stdlib.h>
#include<time.h>

#define MAX_N 10000
const char *file_name = "data3.txt"; 
int arr[MAX_N+5],n=0;

void output_arr(int *arr,int n){
	for(int i=0;i<n;++i){
		printf("%d",arr[i]);
	}
	printf("\n");
	return ;
}

void output_to_file(int *arr,int n){
	FILE *fp = fopen(file_name,"a");
	for(int i=0;i<n;++i){
		fprintf(fp,"%d ",arr[i]);
	}
	fclose(fp);
	return ;
}

int output_test(){
	srand(time(0));
	for(n=0;n<10;n++){
		arr[n]=rand()%100;
	}
	output_arr(arr,n);
	output_to_file(arr,n);
	return 0;
}

int read_from_file(int *arr){
	int i = 0;
	FILE *fp=fopen(file_name,"r");
	if(fp==NULL){
		return 0;
	}
	while(fscanf(fp,"%d",arr+i)!=EOF){
		i+=1;
	}
	return i;
}

void clear_file(){
	FILE *fp = fopen(file_name,"w");
	fclose(fp);
	return ;
}

int main(){
	n=read_from_file(arr);
	output_arr(arr,n);
	printf("total read %d numbers\n",n);
	return 0;
}


