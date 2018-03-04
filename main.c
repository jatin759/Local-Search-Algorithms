#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int mtime, nbids;
int finsel[5000], tempsel[5000], bidssel[5000], tempbid[5000];
//int *bidssel= (int *)malloc(5000 * sizeof(int));

// Finds the conflict between two bids
int **conflict(int **bids, int nbids)
{
    int **admat = (int **)malloc(nbids * sizeof(int *));
    int i=0;
    for(;i<nbids;i++)
    {
        admat[i] = (int *)malloc(nbids * sizeof(int));
    }
    int j,k,l,p=0;
    for(i=nbids-1;i>=0;i--)
    {
        admat[i][i] = 1;
        for(j=0;j<i;j++)
        {
            //If two bids are of same company
            if(bids[i][0]==bids[j][0])
            {
                admat[i][j]=1;
                admat[j][i]=1;
                continue;
            }
            p=0;
            // If two bids have a common block between them
            for(k=3;k<bids[i][1]+3;k++)
            {
                for(l=3;l<bids[j][1]+3;l++)
                {
                    if(bids[i][k]==bids[j][l])
                    {
                        p=1;
                        admat[i][j] = 1;
                        admat[j][i] = 1;
                        break;
                    }
                }
                if(p==1)
                    break;
            }
            // If no conflict
            if(p==0)
            {
                admat[i][j]=0;
                admat[j][i]=0;
            }

        }
    }
    return admat;
}

int randomrestart(int **bids, int **admat, int nbids)
{

    int i ,bsel, num=0;
    int tempnum = 0, p=0, j;
    // selecting a random bid at first;
    bsel = rand() % nbids;
    for(i=0;i<nbids;i++)
    {
        bidssel[i]=-1;
    }
    bidssel[0]=bsel;
    num++;
    //printf("%d\n",bsel);
    while(1)
    {
        //printf("yes\n");
        for(i=0;i<nbids;i++)
        {
            tempbid[i]=-1;
        }
        tempnum = 0;
        p=0;
        // Finding all the neighbours of the current state
        for(i=0;i<nbids;i++)
        {
            p=0;
            for(j=0; bidssel[j]!= -1 && j<nbids ;j++)
            {
                // Neighbour only if there is no conflict
                if(admat[i][bidssel[j]]==1)
                {
                    p=1;
                    break;
                }
            }
            if(p==0)
            {

                tempbid[tempnum] = i;
                tempnum++;
            }
        }
        //printf("%d ",tempnum);
        if(tempnum==0)
            break;

        double aucval = 0.0, maxauc = 0.0;

        /*int finbid;
        // Taking the best neighbour among all neighbours
        for(i=0;tempbid[i]!=-1 && i<nbids;i++)
        {
            aucval = (bids[tempbid[i]][2] * 1.0)/bids[tempbid[i]][1];
            if(maxauc<aucval)
            {
                maxauc=aucval;
                finbid = tempbid[i];
            }
        }*/

        //printf("%d ",num);
        //free(tempbid);
        /*
        // calculating next best neighbour by selecting bid which has maximum value all over.
        double aucval = 0.0, maxauc = 0.0;
        int finbid;
        for(i=0;tempbid[i]!=-1 && i<nbids;i++)
        {
            aucval = (bids[tempbid[i]][2] * 1.0);
            if(maxauc<aucval)
            {
                maxauc=aucval;
                finbid = tempbid[i];
            }
        }
        // Not Giving the best result.
        */

        // Calculating next best neighbour by selecting bid randomly with 0.25 probability
        //and which has maximum value per block with 0.75 prob. respectively.

        int a = rand()%2 , b = rand()%2;
        a = a|b;
        int finbid;
        if(a == 1)
        {
            double aucval = 0.0, maxauc = 0.0;
            for(i=0;tempbid[i]!=-1 && i<nbids;i++)
            {
                aucval = (bids[tempbid[i]][2] * 1.0)/bids[tempbid[i]][1];
                if(maxauc<aucval)
                {
                    maxauc=aucval;
                    finbid = tempbid[i];
                }
            }
        }
        else
        {
            int rd = rand()%tempnum;
            finbid = tempbid[rd];
        }
        // Giving best result.
        bidssel[num] = finbid;
        num++;

    }

    int revenue =0;

    for(i=0;i<nbids;i++)
    {
        tempsel[i] = -1;
    }
    // Calculating the total revenue
    for(i=0;i<num && bidssel[i]!= -1 ;i++)
    {
        revenue += bids[bidssel[i]][2];
        tempsel[i] = bidssel[i];
    }
    //printf("yes\n");
    return revenue;
}

int hillclimb(int **bids, int **admat, int nbids)
{
    int maxrevenue=0,i;
    double extime;
    clock_t start,end;
    start = clock();
    while(1)
    {
        end=clock();
        extime=((double)(end-start))/CLOCKS_PER_SEC;
        // If time out then break the loop
        if(extime > mtime*60)
            break;
        double temp = clock()/CLOCKS_PER_SEC;
        //printf("%f\n",temp);
        //printf("%d\n",maxrevenue);
        int revenue = randomrestart(bids, admat, nbids);
        if(revenue>maxrevenue)
        {
            // Taking max revenue among all the revenues obtained
            maxrevenue = revenue;
            for(i=0;i<nbids;i++)
            {
                finsel[i] = -1;
            }
            // The bids which got selected
            for(i=0;tempsel[i]!=-1;i++)
            {
                finsel[i] = tempsel[i];
            }
        }

    }
    return maxrevenue;
}

int main(int argc, char *argv[])
{
    srand (time(NULL));

    int i,nblocks,ncomp,cid,ncid;

    char buff[255];

    FILE *fp, *fot;

    //fp = fopen("p1/7.txt","r");
    fp = fopen(argv[1],"r");
    fot= fopen(argv[2],"w");
    fscanf(fp,"%d", &mtime);
    fscanf(fp,"%d", &nblocks);
    fscanf(fp,"%d", &nbids);
    fscanf(fp,"%d", &ncomp);

    //int *bids[nbids];
    //bids = new int*[nbids];
    int **bids = (int **)malloc(nbids * sizeof(int *));

    int b,bval,block,j;

    for(i=0;i<nbids;)
    {
        fscanf(fp, "%d", &cid);
        fscanf(fp, "%d", &ncid);
        while(ncid)
        {
            fscanf(fp, "%d", &cid);
            fscanf(fp, "%d", &b);
            fscanf(fp, "%d", &bval);

            bids[i] = (int *)malloc((b+3) * sizeof(int));
            //int ar[b+3];
            bids[i][0] = cid;
            bids[i][1] = b;
            bids[i][2] = bval;
            j=3;
            while(j<b+3)
            {
                fscanf(fp, "%d", &block);
                bids[i][j] = block;
                j++;
            }

            i++;
            ncid--;
        }
    }

    // 2D array which tell the conflict between two bids
    int **admat = conflict(bids, nbids);

    int maxrevenue = hillclimb(bids, admat, nbids);

    // Final ans
    fprintf(fot,"%d ",maxrevenue);
    for(i=0 ; i<nbids && finsel[i]!= -1 ; i++)
    {
        fprintf(fot,"%d ",finsel[i]);
    }
    fprintf(fot,"\n");

    /*int *chk = (int *)malloc(nbids * sizeof(int));
    chk[0] = -1;
    for(i=0;i<nbids;i++)
    {
        printf("%d ",chk[i]);
    }*/
    /*int l;
    for(i=0;i<nbids;i++)
    {
        //l = bids[i][1];
        for(j=0;j<nbids;j++)
        {
            printf("%d ",admat[i][j]);
        }
        printf("\n");
    }*/

    return 0;

}
