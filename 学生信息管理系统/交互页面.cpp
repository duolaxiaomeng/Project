#include<stdio.h>
#include<stdlib.h>
#define MAX_N 10000
const char *file_name="student_data.txt";


typedef struct Student{
	char name[20];
	int age;
	int classes;
	double height;
} Student;



Student stus[MAX_N+5];
int scnt;

int read_from_file(Student *arr){
	int i = 0;
	FILE *fp=fopen(file_name,"r");
	if(fp==NULL){
		return 0;
	}
	while(fscanf(fp,"%s",arr[i].name)!=EOF){
		fscanf(fp,"%d%d%lf",&arr[i].age,&arr[i].classes,&arr[i].height);
		i+=1;
	}
	return i;
}

void output_arr(int *arr,int n){
	for(int i=0;i<n;++i){
		printf("%d",arr[i]);
	}
	printf("\n");
	return ;
}

void output_to_file(Student *arr,int n){
	FILE *fp = fopen(file_name,"a");
	for(int i=0; i<n; ++i){
		fprintf(fp,"%s %d %d %.2lf\n",arr[i].name,
									arr[i].age,
									arr[i].classes,
									arr[i].height);
	}
	fclose(fp);
	return ;
}


void List_students(){
	int len = printf("%4s|%10s|%4s|%6s|%7s","id","name","age","class","height");
	printf("\n");
	for(int i=0;i<len;++i)printf("=");
	printf("\n");
	for(int i=0;i<scnt;++i){
		printf("%4d|%10s|%4d|%6d|%7.2lf|\n",
		i,
		stus[i].name,
		stus[i].age,
		stus[i].classes,
		stus[i].height
		);
	}
	return ;
}

void add_a_student(){
	printf("add new item : (name,age,class,height)\n");
	printf("mysql > ");
	scanf("%s%d%d%lf",
		&stus[scnt].name,
		&stus[scnt].age,
		&stus[scnt].classes,
		&stus[scnt].height
	);
	output_to_file(stus + scnt, 1);
	scnt += 1;
	printf("add a new stydent success\n");
	return ;
}

void clear_file(){
	FILE *fp = fopen(file_name,"w");
	fclose(fp);
	return ;
}

void restor_data_to_file(Student *arr,int n){
	clear_file();
	output_to_file(arr,n);
	
	
	return ;
}



void modify_a_student(){
	List_students();
	int id;
	do{
	printf("modify id : ");
	scanf("%d",&id);
	}while(id < 0 || id >= scnt);
	printf("modify a item : (name,age,class,height)\n");
	printf("mysql > ");
	scanf("%s%d%d%lf",
		&stus[id].name,
		&stus[id].age,
		&stus[id].classes,
		&stus[id].height
	);
	restor_data_to_file(stus,scnt);
	return ;
}


enum NO_TYPE {
	LIST=1,
	ADD,
	MODIFY,
	DELETE,
	QUIT
};


int usage(){
	int no;
	do{
	
	printf("%d : list students\n",LIST);
	printf("%d : add a new students\n",ADD);
	printf("%d : modify a students\n",MODIFY);
	printf("%d : delete a students\n",DELETE);
	printf("%d : quit\n",QUIT);
	printf("mysql > ");
	scanf("%d",&no);
	return no;
	}while(no < LIST || no > QUIT);
}

void delete_a_student(){
	if(scnt == 0){
		printf("there is no student\n");
		return ;
	}
	List_students();
	int id;
	do{
	printf("delete id : ");
	scanf("%d",&id);
	}while(id < 0 || id >= scnt);
	char s[100];
	printf("confim (y / n): ");
	fflush(stdin);
	scanf("%[^/n]",s);
	if(s[0] == 'n')return;
	printf("mysql > ");
	for(int i = id+1;i<scnt;++i){
		stus[i-1] = stus[i];
	}
	scnt--;
	restor_data_to_file(stus,scnt);
	return ;
}

int main(){
	scnt = read_from_file(stus);
	while(1){
		int no=usage();
		switch(no){
			case LIST:{
				List_students();
				break;
			}
			case ADD:printf("2\n");{
				add_a_student();
				break;
			}
			case MODIFY:{
				modify_a_student();
				break;
			}
			case DELETE:{
				delete_a_student();
				break;
			}
			case QUIT:printf("5\n");exit(0);		
		}
		
	}
	return 0;
}
